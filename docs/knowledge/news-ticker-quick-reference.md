# News Ticker Design: Quick Reference

**Companion to**: [News Ticker Design Patterns: Comparative Analysis](news-ticker-design-patterns.md)

## Position Strategy

```
┌─────────────────────────────────────┐
│  TOP: Breaking News (Discovery)     │ ← CNN, BBC banners
│  - Urgent, attention-grabbing       │
│  - Red/high contrast colors         │
│  - Interrupts user flow             │
├─────────────────────────────────────┤
│                                     │
│     MAIN CONTENT AREA               │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  BOTTOM: Ambient (Monitoring)       │ ← CNBC, ESPN tickers
│  - Glanceable, non-intrusive        │
│  - Constant scroll or flip          │
│  - Doesn't interrupt main task      │
└─────────────────────────────────────┘
```

## Animation Patterns

### Old School (Declining)
```
Continuous scroll →→→→→→→→→→→→→→→
Problem: Catch end of item, wait for loop
```

### Modern (Preferred)
```
┌────────┐    ┌────────┐    ┌────────┐
│ Item 1 │ → flip → │ Item 2 │ → flip → │ Item 3 │
└────────┘    └────────┘    └────────┘
Benefit: Full info visible, no waiting
```

## Color Coding (Financial)

| Color | Western Markets | Asian Markets |
|-------|----------------|---------------|
| 🟢 Green | ↑ Rising | ↓ Falling |
| 🔴 Red | ↓ Falling | ↑ Rising |
| ⚪ White/Gray | → Unchanged | → Unchanged |

## Essential Interactions

1. **Pause on Hover** (non-negotiable)
   ```css
   .ticker:hover { animation-play-state: paused; }
   ```

2. **Click to Expand**
   - Inline for low priority
   - Modal for breaking news

3. **Keyboard Navigation**
   - Tab through items
   - Space to pause/play
   - Arrow keys to navigate

## Speed Guidelines

| Speed | Effect | Use Case |
|-------|--------|----------|
| Too Fast | Eye strain, unreadable | ❌ Avoid |
| Optimal | Engagement + comprehension | ✅ Target |
| Too Slow | Boredom, users leave | ❌ Avoid |

**Research finding**: 60% better retention on dynamic displays vs static (when speed is optimized)

## Notification Severity

```
┌──────────────────────────────────────┐
│ HIGH: Modal (blocks interaction)     │ Critical alerts
├──────────────────────────────────────┤
│ MEDIUM: Banner (dismissible)         │ Important updates
├──────────────────────────────────────┤
│ LOW: Toast (auto-dismiss)            │ Informational
└──────────────────────────────────────┘
```

## Mobile Considerations

| Challenge | Solution |
|-----------|----------|
| Limited vertical space | Single line ticker |
| Horizontal scroll conflicts | Tap-to-advance instead |
| Touch targets too small | Larger tap areas (44px min) |
| Reduced attention span | Shorter content chunks |

## Organization Patterns

| Organization | Position | Content | Speed | Use |
|--------------|----------|---------|-------|-----|
| **CNN** | Top banner | Breaking news | Static reveal | Discovery |
| **BBC** | Bottom reveal | Live updates | Static reveal | Discovery |
| **Reuters** | Embedded | News + audio | Variable | Both |
| **CNBC** | Bottom + static line | Financial data | Constant scroll | Monitoring |
| **ESPN** | Bottom | Sports scores | Flip animation | Monitoring |
| **Al Jazeera** | Embedded stream | Social + news | Continuous feed | Both |

## Personalization Architecture

```
User Input
    │
    ├─→ Content-Based Filtering (similar articles)
    │
    ├─→ Collaborative Filtering (similar users)
    │
    └─→ Hybrid Model (best results)
            │
            ├─→ User Control Panel
            │   ├─ Source preferences
            │   ├─ Topic filters
            │   ├─ Personalization level
            │   └─ "Show diverse content" toggle
            │
            └─→ Filtered Ticker Output
```

## Design Evolution Timeline

```
1995 ──────────── 2018 ──────────── 2023 ──────────── 2026
│                 │                 │                 │
ESPN BottomLine   ESPN flip         CNBC flat         Prediction markets
(constant scroll) (discrete items)  (minimalist)      (CNN/CNBC + Kalshi)
```

## Anti-Patterns ❌

1. **No pause mechanism** → Frustrating
2. **Too much visual decoration** → Cluttered
3. **Hidden content without signposting** → Users miss items
4. **Auto-play with sound** → Intrusive
5. **Notification overload** → Users disable all
6. **No keyboard/screen reader support** → Accessibility failure

## Implementation Checklist

- [ ] Position appropriate for use case (top = discovery, bottom = monitoring)
- [ ] Pause on hover
- [ ] Keyboard navigation (Tab, Space, Arrows)
- [ ] Screen reader support (ARIA labels, focus management)
- [ ] Mobile responsive (not just scaled down)
- [ ] Color coding (if financial/status data)
- [ ] Clear visual hierarchy
- [ ] Limit text per item
- [ ] Click to expand/navigate
- [ ] User control (pause, filter, personalize)
- [ ] Performance optimized (CSS animations, lazy load)
- [ ] Respects reduced motion preferences
- [ ] High contrast mode compatible

## Performance Targets

| Metric | Target |
|--------|--------|
| First paint | < 100ms |
| Animation FPS | 60 FPS |
| CPU usage | < 5% idle |
| Memory footprint | < 10MB |
| Network requests | Batch updates |

## Content Strategy

```
Headline Structure:
[URGENCY BADGE] [SOURCE] [HEADLINE] [TIMESTAMP]

Example:
🔴 BREAKING | Reuters | Major policy announcement | 2m ago
```

**Guidelines**:
- Headline max: 80 characters
- Most important info first
- Clear attribution
- Relative timestamps (2m ago, 1h ago)
- Link to full article

## Discovery vs Monitoring

### Discovery
- **When**: User needs to know NOW
- **Where**: Top of screen
- **How**: Interrupting, modal/banner
- **Content**: Heterogeneous, breaking news
- **Examples**: CNN banners, BBC alerts

### Monitoring
- **When**: Background awareness
- **Where**: Bottom of screen
- **How**: Ambient, non-interrupting
- **Content**: Homogeneous, continuous
- **Examples**: CNBC stocks, ESPN scores

### Hybrid
- **Primary**: Monitoring
- **Override**: Discovery (breaking news takes over)
- **Example**: CNBC ticker switches to breaking business news

## Next Steps for Implementation

1. Choose mode: Discovery, Monitoring, or Hybrid
2. Select position based on mode
3. Design animation (prefer flip over scroll)
4. Implement pause-on-hover
5. Add keyboard navigation
6. Build mobile-responsive variant
7. Test accessibility (screen reader, keyboard, reduced motion)
8. Optimize performance
9. User test for readability and speed
10. Iterate based on feedback

---

**See full analysis**: [News Ticker Design Patterns: Comparative Analysis](news-ticker-design-patterns.md)
