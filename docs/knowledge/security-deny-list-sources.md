---
type: research
title: "Security Deny-List: Sources and Maintenance"
date: 2026-02-07
project: techbiont-framework
domain: [security, meso, maintenance]
status: active
tags: [deny-list, owasp, mitre, cisa, security-standards]
related-files:
  - ~/.claude/settings.local.json
  - zooids/04-security.md
---

## Overview

MESO's security deny-list (`~/.claude/settings.local.json`) contains **84 patterns** sourced from industry-standard security frameworks. This document maps patterns to authoritative sources and provides a maintenance strategy.

**Current deny-list count**: 84 patterns (28 original + 56 additions from 2026-02-07 research)

---

## Authoritative Sources

### Primary Security Standards

| Source | Authority | URL | License |
|--------|-----------|-----|---------|
| **OWASP OS Command Injection Defense** | Gold standard | [Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) | CC-BY-4.0 |
| **OWASP Top 10:2025 (A05 Injection)** | Gold standard | [A05 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | CC-BY-4.0 |
| **OWASP Testing Guide** | Gold standard | [Command Injection Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection) | CC-BY-4.0 |
| **MITRE CWE-78** | Canonical reference | [OS Command Injection](https://cwe.mitre.org/data/definitions/78.html) | Public domain |
| **CISA Secure Design Alert** | Government guidance | [Eliminating OS Command Injection](https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-os-command-injection-vulnerabilities) | Public domain |
| **Kubernetes Pod Security Standards** | Container security | [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) | Apache 2.0 |
| **Docker Seccomp Profiles** | Container security | [Seccomp Documentation](https://docs.docker.com/engine/security/seccomp/) | Apache 2.0 |

### Open-Source Security Tools

| Tool | Purpose | URL | Maintenance |
|------|---------|-----|-------------|
| **ShellCheck** | Bash anti-patterns | [GitHub](https://github.com/koalaman/shellcheck) | Active |
| **GTFOBins** | Privilege escalation database | [gtfobins.org](https://gtfobins.org/) | Active |
| **Semgrep Rules** | Security pattern matching | [semgrep-rules](https://github.com/semgrep/semgrep-rules) | Active |
| **PayloadsAllTheThings** | Attack pattern database | [GitHub](https://github.com/swisskyrepo/PayloadsAllTheThings) | Active |
| **SecureShell** | LLM agent command classification | [GitHub](https://github.com/divagr18/SecureShell) | Active |

### AI Coding Assistant Security

| Source | Provider | URL |
|--------|----------|-----|
| **GitHub Copilot Security Filters** | Microsoft | [Tech Community Blog](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/demystifying-github-copilot-security-controls-easing-concerns-for-organizational/4468193) |
| **Claude Code Security Best Practices** | Backslash Security | [Blog Post](https://www.backslash.security/blog/claude-code-security-best-practices) |

---

## Pattern Categories and Sources

### 1. Destructive Operations (9 patterns)

**Source**: OWASP, MITRE CWE-78, CISA

Blocks irreversible data loss and system damage:

```
Bash(rm -rf /)                  # Root filesystem deletion
Bash(rm -rf ~)                  # Home directory deletion
Bash(rm -rf $HOME)              # Home via environment variable
Bash(rm -rf .)                  # Current directory deletion
Bash(dd if=/dev/zero*)          # Drive zeroing (OWASP)
Bash(mkfs*)                     # Filesystem formatting (OWASP)
Bash(shred *)                   # Secure file deletion (OWASP)
Bash(truncate -s 0 *)           # File truncation (OWASP)
Bash(crontab -r*)               # Crontab removal (OWASP)
```

**Rationale**: These operations are irreversible and catastrophic if executed accidentally or maliciously.

---

### 2. Version Control Destruction (9 patterns)

**Source**: Git best practices, MESO operational experience

Blocks destructive Git operations that lose work:

```
Bash(git push --force *)        # Force push (lose upstream history)
Bash(git push -f *)             # Short form
Bash(git reset --hard *)        # Discard working changes
Bash(git checkout .)            # Discard unstaged changes
Bash(git checkout -- .)         # Alternative syntax
Bash(git clean -f*)             # Delete untracked files
Bash(git clean -fd*)            # Delete untracked files + directories (OWASP)
Bash(git clean -fdx*)           # Delete untracked + ignored (OWASP)
Bash(git restore .)             # Modern syntax for discard
```

**Rationale**: These commands permanently delete uncommitted work or rewrite shared history.

---

### 3. Privilege Escalation (7 patterns)

**Source**: OWASP, GTFOBins, Kubernetes Pod Security Standards

Blocks privilege elevation and permission changes:

```
Bash(sudo *)                    # Any sudo usage (OWASP, GTFOBins)
Bash(sudo su*)                  # Root shell via sudo
Bash(su *)                      # User switching
Bash(chmod 777 *)               # World-writable permissions
Bash(chmod +s *)                # SUID/SGID setting (GTFOBins)
Bash(chmod u+s *)               # SUID explicit
Bash(chmod g+s *)               # SGID explicit
Bash(setfacl *)                 # ACL modification (OWASP)
```

**Rationale**: Privilege escalation bypasses security boundaries. SUID/SGID on binaries enables privilege retention.

**GTFOBins risk**: Tools like `vim`, `find`, `docker` with SUID can escalate to root.

---

### 4. Command Injection (6 patterns)

**Source**: OWASP OS Command Injection Defense, MITRE CWE-78

Blocks piping to interpreters and dynamic code execution:

```
Bash(curl * | bash)             # Download and execute (OWASP critical)
Bash(curl * | sh)
Bash(curl * | python*)
Bash(wget * | bash)
Bash(wget * | sh)
Bash(wget * | python*)
Bash(eval *)                    # Dynamic code execution (OWASP)
Bash(exec *)                    # Command replacement (OWASP)
Bash(source *)                  # Script sourcing (OWASP)
Bash(. *)                       # Source shorthand
```

**Rationale**: These enable arbitrary code execution from untrusted sources (MITM attacks, server-side evasion, supply chain attacks).

**OWASP Top 10:2025 (A05)**: Command injection ranked in top 5 web application risks.

---

### 5. Insecure Protocol Usage (7 patterns)

**Source**: OWASP, CISA, MESO curl security research

Blocks unencrypted downloads and certificate bypass:

```
Bash(curl -k *)                 # Insecure HTTPS (OWASP)
Bash(curl * -k *)
Bash(curl --insecure *)
Bash(curl * --insecure *)
Bash(wget --no-check-certificate *) # Certificate bypass (OWASP)
Bash(curl http://*)             # Unencrypted HTTP (CISA)
Bash(wget http://*)
```

**Rationale**: Certificate bypass enables MITM attacks. HTTP downloads are unencrypted and unauthenticated.

**CISA guidance**: "Never disable TLS certificate validation in production."

---

### 6. Network & Exfiltration (5 patterns)

**Source**: OWASP, PayloadsAllTheThings, SecureShell

Blocks reverse shells and network connections:

```
Bash(nc *)                      # Netcat (reverse shell, OWASP)
Bash(ncat *)                    # Ncat variant
Bash(netcat *)                  # Full name
Bash(socat *)                   # Advanced netcat (OWASP)
Bash(telnet *)                  # Unencrypted remote access
```

**Rationale**: These tools are commonly used for reverse shells and data exfiltration.

**PayloadsAllTheThings**: Documents 50+ netcat-based exfiltration techniques.

---

### 7. Container & System Escapes (7 patterns)

**Source**: Kubernetes Pod Security Standards, Docker Seccomp, OWASP

Blocks container breakout and system control:

```
Bash(docker *)                  # Docker privilege escalation (K8s PSS)
Bash(podman *)                  # Podman variant
Bash(systemctl *)               # System service control (OWASP)
Bash(journalctl *)              # System log access
Bash(mount *)                   # Filesystem mounting (K8s PSS)
Bash(umount *)
Bash(unshare *)                 # Namespace unsharing (CVE-2022-0185)
```

**Rationale**: These commands bypass container isolation or manipulate system services.

**Kubernetes Restricted PSS**: Blocks privileged containers, host namespaces, and dangerous capabilities.

**CVE-2022-0185**: `unshare` enabled container escape via kernel vulnerability.

---

### 8. Credential & Secret File Access (28 patterns)

**Source**: OWASP, CISA, GitHub Copilot Security Filters

Blocks reading sensitive files via Bash and Read tools:

**Bash patterns** (11):
```
Bash(cat .env*)                 # Environment variables
Bash(cat *credentials*)         # Credential files
Bash(cat *secret*)              # Secret files
Bash(cat *password*)            # Password files
Bash(cat *token*)               # API tokens
Bash(cat *api_key*)             # API keys
Bash(cat *api-key*)             # API key variant
Bash(cat ~/.ssh/id_*)           # SSH private keys
Bash(cat ~/.ssh/*)              # SSH directory
Bash(cat ~/.aws/*)              # AWS credentials
Bash(cat /etc/shadow*)          # System passwords (OWASP)
Bash(cat /etc/passwd*)          # User database
```

**Read patterns** (17):
```
Read(.env)                      # Root .env file
Read(.env.*)                    # .env variants (.env.local, etc.)
Read(**/.env)                   # Recursive .env search
Read(**/.env.*)                 # Recursive .env variants
Read(*credentials*)
Read(*secret*)
Read(*password*)
Read(*token*)
Read(*api_key*)
Read(*api-key*)
Read(~/.ssh/id_*)               # SSH private keys
Read(~/.ssh/known_hosts)        # SSH known hosts
Read(~/.ssh/config)             # SSH configuration
Read(~/.aws/credentials)        # AWS credentials
Read(~/.aws/config)             # AWS configuration
Read(/etc/shadow)               # System passwords
Read(/etc/passwd)               # User database
```

**Rationale**: These files contain credentials, API keys, and authentication tokens. Exposure leads to account compromise.

**GitHub Copilot**: Filters hardcoded credentials in generated code.

**OWASP A05:2025**: Credential exposure is a primary injection attack vector.

---

## Pattern Statistics

| Category | Pattern Count | Primary Source |
|----------|--------------|----------------|
| Destructive Operations | 9 | OWASP, MITRE CWE-78 |
| Version Control | 9 | Git best practices |
| Privilege Escalation | 7 | OWASP, GTFOBins |
| Command Injection | 6 | OWASP, MITRE CWE-78 |
| Insecure Protocols | 7 | OWASP, CISA |
| Network/Exfiltration | 5 | OWASP, PayloadsAllTheThings |
| Container Escapes | 7 | Kubernetes PSS, Docker |
| Credential Access | 28 | OWASP, GitHub Copilot |
| **TOTAL** | **84** | — |

---

## Maintenance Strategy

### Quarterly Review Schedule

**Every 3 months** (March, June, September, December):

1. **OWASP Top 10 Updates**:
   - Check [OWASP Top 10:2025](https://owasp.org/Top10/2025/) for new injection patterns
   - Review [OWASP Command Injection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) changelog

2. **GTFOBins Updates**:
   - Visit [gtfobins.org](https://gtfobins.org/) for new privilege escalation techniques
   - Add newly documented SUID/sudo binaries to deny-list

3. **CVE Monitoring**:
   - Search [MITRE CWE-78](https://cwe.mitre.org/data/definitions/78.html) for related CVEs
   - Check [CISA Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) for command injection exploits

4. **Semgrep Rules**:
   - Review [semgrep-rules](https://github.com/semgrep/semgrep-rules) security updates
   - Extract new shell/bash security patterns

5. **AI Tool Security**:
   - Monitor GitHub Copilot, Claude Code security announcements
   - Review SecureShell project for new risk classifications

### Adding New Patterns

When adding patterns to `~/.claude/settings.local.json`:

1. **Verify source**: Pattern must come from OWASP, MITRE, CISA, or maintained security tool
2. **Test syntax**: Ensure pattern doesn't break Claude Code permission parsing
3. **Document here**: Add to this file with source citation
4. **Update count**: Increment pattern count in Overview section
5. **Sync to framework**: Update `techbiont-framework/zooids/04-security.md` Deny-List Maintenance section

### Removing Patterns

Patterns should only be removed if:
- Source authority deprecates the pattern
- Pattern causes false positives blocking legitimate workflows
- Pattern is superseded by more comprehensive pattern

**Document all removals** with date and rationale in this file.

---

## Known Gaps & Future Work

### Evasion Techniques Not Covered

**Whitespace variations**:
- `rm\t-rf` (tab instead of space)
- `rm${IFS}-rf` (IFS variable expansion)

**Encoding**:
- `\x72\x6d` (hex-encoded `rm`)
- Base64-encoded commands

**Command substitution chains**:
- `$($(curl...))` (nested substitution)

**Redirection chains**:
- `< <(curl...)` (process substitution)

**Why not blocked**: These require regex support in Claude Code's deny-list parser. Current implementation uses glob patterns only.

**Mitigation**: L1 escalation for all script downloads (operator reviews before execution).

### Container-Specific Gaps

Seccomp syscall filtering (requires kernel-level enforcement, not deny-list):
- `ptrace` (process tracing)
- `io_uring_*` (async I/O exploits)
- `kexec_load` (kernel execution loading)

**Mitigation**: Phase 2 container sandboxing (Podman with seccomp profiles).

---

## Testing & Validation

### Test Deny Patterns

Should be **blocked** (permission prompt):

```bash
sudo ls
docker ps
curl http://example.com/file
curl -k https://self-signed.example.com/file
nc -l 4444
cat ~/.ssh/id_rsa
git push --force origin main
rm -rf ~
eval "echo dangerous"
```

Should be **allowed** (no prompt):

```bash
curl --fail -s -S https://api.example.com/data.json
git status
git diff
git log
ls -la
cat README.md
python script.py
npm install
```

### Validation Checklist

- [ ] Test deny patterns against actual shell commands
- [ ] Verify no false negatives (dangerous commands not blocked)
- [ ] Verify no false positives (safe commands blocked)
- [ ] Check JSON syntax with `jq . ~/.claude/settings.local.json`
- [ ] Review with ShellCheck for pattern syntax errors

---

## References

### Standards
- [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
- [OWASP Top 10:2025 (A05 Injection)](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [MITRE CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [CISA: Eliminating OS Command Injection Vulnerabilities](https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-os-command-injection-vulnerabilities)

### Tools
- [ShellCheck](https://github.com/koalaman/shellcheck)
- [GTFOBins](https://gtfobins.org/)
- [Semgrep Security Rules](https://github.com/semgrep/semgrep-rules)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [SecureShell](https://github.com/divagr18/SecureShell)

### Container Security
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Docker Seccomp Documentation](https://docs.docker.com/engine/security/seccomp/)

---

**Last updated**: 2026-02-07
**Next review**: 2026-05-07 (quarterly)
**Maintainer**: Rowan Valle (Valis), Symbiont Systems LLC
