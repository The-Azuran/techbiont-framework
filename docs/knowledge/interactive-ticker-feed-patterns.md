---
title: Interactive Ticker and Feed Patterns
date: 2026-02-07
author: Rowan Valle
domain: ux, patterns, real-time, interaction-design
status: research
---

# Interactive Ticker and Feed Patterns: Pattern Library

Research synthesis on interactive continuous data stream implementations in modern web applications. Organized by interaction paradigm, emphasizing patterns that support discovery versus monitoring use cases.

## Executive Summary

Interactive feeds fall along two primary axes:

1. **Purpose**: Discovery (browsing, exploration) vs Monitoring (awareness, alerts)
2. **Attention**: Ambient (peripheral awareness) vs Focused (primary task)

The most successful implementations match interaction patterns to user intent. Discovery-focused applications use infinite scroll with rich filtering. Monitoring applications use pause/resume controls, speed adjustment, and ambient notification patterns.

## Core Interaction Paradigms

### 1. Discovery-Focused Feeds

**Goal**: Help users find interesting content they didn't know they were looking for.

**Characteristics**:
- Infinite scroll with minimal friction
- Algorithm-driven relevance ranking
- Rich filtering and categorization
- Read/unread state tracking
- Bookmark/save for later functionality

**Applications**:
- Social media (Twitter/X, Instagram, Reddit)
- News aggregators (Feedly, Inoreader)
- Content platforms (YouTube, TikTok)

### 2. Monitoring-Focused Feeds

**Goal**: Provide awareness of real-time changes without demanding continuous attention.

**Characteristics**:
- Pause/resume controls with two resume strategies
- Speed/velocity controls
- Visual indicators for state changes (green/red, bold/unbold)
- Ambient notifications vs alerts
- Time-based landmarks

**Applications**:
- Trading platforms (TradingView, stock tickers)
- Live events (Twitch chat, Reddit live threads)
- Productivity tools (Slack, Linear, GitHub)

### 3. Hybrid Approaches

**Goal**: Support both discovery and monitoring within a single interface.

**Characteristics**:
- Tabbed or multi-stream layouts
- Context-switching between modes
- Customizable notification thresholds
- Multi-level filtering (global + per-stream)

**Applications**:
- Discord (activity feed + channels)
- Notion (activity log + content browsing)
- Multi-stream dashboards (Dynamics 365)

---

## Pattern Catalog

### Pattern 1: Pause/Resume Control

**Context**: Real-time feeds where information becomes stale or misleading if paused.

**Implementation**:

Two distinct resume strategies based on content type:

1. **Resume from pause point** (Non-real-time content)
   - Use case: Reading articles, browsing social posts
   - Behavior: Pause freezes the stream; resume continues from frozen point
   - User need: "I want to finish reading this item"

2. **Jump to current on resume** (Real-time status content)
   - Use case: Stock tickers, weather radar, auction timers, traffic cameras
   - Behavior: Pause freezes display; resume jumps to current state
   - User need: "I need current information, not stale data"
   - Critical: Display "delayed" notice when paused

**Accessibility requirement** (WCAG 2.2.2):
- Moving, blinking, scrolling content lasting >5 seconds MUST provide pause/stop/hide controls
- Applies to: stock tickers, news tickers, auto-scrolling feeds

**Example implementations**:
- Stock ticker: Pause button shows current stock, restart shows notice "display is delayed"
- Twitch chat: Pause button stops scroll, new messages buffer, resume jumps to latest

**Sources**:
- [WCAG 2.2.2: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG21/Understanding/pause-stop-hide.html)
- [Framer community: Play/pause controls on ticker](https://www.framer.community/c/support/p-lay-pause-controls-on-ticker-component)

---

### Pattern 2: Speed/Velocity Control

**Context**: Users need to control information flow rate based on cognitive load and monitoring intensity.

**Implementation**:

Velocity controls adjust scroll/update speed without pausing the feed.

**Typical speed ranges**:
- 0.25x (slow monitoring, detailed reading)
- 0.5x (relaxed monitoring)
- 1x (default, balanced for most users)
- 1.5x (fast scanning)
- 2x+ (rapid overview, expert users)

**Visual feedback**:
- Speed indicator always visible
- Smooth acceleration/deceleration (no jarring jumps)
- Animation easing curves for natural feel

**Cognitive considerations**:
- Slower speeds: Better comprehension, lower anxiety
- Faster speeds: Higher cognitive load, risk of missing information
- User-controlled: Supports both expert and novice users

**Implementation notes**:
- CSS animation-duration for ticker tapes
- JavaScript frame rate control for dynamic feeds
- WebSocket throttling for data-heavy streams

**Sources**:
- [CSS Ticker with hover pause](https://codepen.io/donnchadh/pen/poyvzog)
- [CodyHouse Ticker component](https://codyhouse.co/ds/components/info/ticker)

---

### Pattern 3: Infinite Scroll vs Pagination

**Context**: Choosing between continuous flow and discrete pages based on user goals.

**Infinite Scroll**:

**Best for**:
- Discovery-based browsing (social media, image galleries)
- User-generated content streams (Twitter, Instagram, Pinterest)
- Entertainment and news consumption
- Mobile interfaces (continuous thumb scroll)

**Strengths**:
- Reduces interruptions and cognitive breaks
- Creates "flow state" for engagement
- Lower friction for browsing
- Optimal for touch interfaces

**Weaknesses**:
- Lack of landmarks (hard to return to specific item)
- No sense of completion ("infinite" feels endless)
- Footer becomes unreachable
- Poor for goal-oriented searches
- SEO challenges (content not indexable)

**Research finding**: "Continuous attention where the brain locks into a rhythm—each new item requires minimal re-engagement, making feeds feel frictionless."

**Pagination**:

**Best for**:
- Goal-oriented searches (shopping, research, job hunting)
- Content that requires comparison
- When users need to bookmark/share specific locations
- When total result count matters

**Strengths**:
- Cognitive anchors (page numbers)
- Sense of control and completion
- Easy to return to specific items
- Better for SEO
- Footer remains accessible

**Weaknesses**:
- Interruptions break flow
- Requires explicit action to continue
- Can feel slow on mobile

**Hybrid solution: "Load More" button**:
- Combines benefits of both approaches
- Gives users small milestones
- Prevents endless page growth
- Works well on mobile
- User controls pace of loading

**Research finding**: "Even short interruptions can trigger users to change tasks. Minimizing interruptions is important for social media, entertainment, and news sites."

**Decision matrix**:

| User Goal | Content Type | Recommend |
|-----------|--------------|-----------|
| Browse/discover | User-generated, timeline-based | Infinite scroll |
| Search for specific item | Product catalog, job listings | Pagination |
| Compare options | E-commerce, research | Pagination |
| Entertainment | Videos, images, social posts | Infinite scroll |
| Return to specific item | Documentation, forums | Pagination |
| Mobile-first | Any | Infinite scroll or "Load More" |

**Sources**:
- [UX Planet: Infinite Scrolling vs. Pagination](https://uxplanet.org/ux-infinite-scrolling-vs-pagination-1030d29376f1)
- [LogRocket: Pagination vs infinite scroll UX](https://blog.logrocket.com/ux-design/pagination-vs-infinite-scroll-ux/)
- [Nielsen Norman Group: Infinite Scrolling Tips](https://www.nngroup.com/articles/infinite-scrolling-tips/)

---

### Pattern 4: Read/Unread State Management

**Context**: Tracking what users have seen across devices and sessions.

**Implementation approaches**:

**1. Backend flag tracking**:
- Each item has viewed/unread flag per user
- Visual cues: bold text, colored dots, badges
- State persists across sessions and devices

**2. Per-conversation state** (messaging/collaboration):
- JSON dictionary of timestamps per conversation/channel
- Messages older than timestamp = unread
- Real-time sync across devices via pub/sub

**3. Cross-device synchronization**:
- User subscribes to state-change channel
- Mark as read/unread/archive propagates instantly
- WebSocket or pub/sub for real-time updates

**Visual indicators**:

- **Numeric badges**: Exact unread count (Slack, email)
- **Binary status**: Simple read/unread indicator (Twitter, Reddit)
- **Chronological markers**: "New since last login", timestamps
- **Color coding**: Unread items in bold or highlighted

**State-change actions**:

Users must be able to:
- Mark as read/unread
- Archive (hide from main feed but preserve)
- Delete (permanent removal)
- Bulk actions (mark all as read)

**Platform-specific considerations**:

**Mobile**:
- Compact indicators (limited screen space)
- Swipe gestures for quick state changes
- Platform notification integration (iOS, Android)

**Desktop**:
- Detailed indicators with hover states
- Keyboard shortcuts (j/k navigation, r for read)
- Richer information density
- Hover previews

**Implementation pattern** (pseudo-code):

```javascript
// Per-user read state
{
  user_id: "abc123",
  conversations: {
    "channel_1": { last_read: "2026-02-07T10:30:00Z" },
    "channel_2": { last_read: "2026-02-07T09:15:00Z" }
  }
}

// Message unread check
function isUnread(message, channel_id) {
  const lastRead = user.conversations[channel_id].last_read;
  return message.timestamp > lastRead;
}

// Update on read (broadcast to all user devices)
pubsub.publish(`user:${user_id}:read_state`, {
  channel: channel_id,
  timestamp: new Date().toISOString()
});
```

**Sources**:
- [SuprSend: Activity Feed Design](https://www.suprsend.com/post/activity-feed)
- [PubNub: Read Receipts Pattern](https://scalabl3.github.io/pubnub-design-patterns/2017/04/19/Read-Receipts.html)
- [GetStream: Activity Feed Design Guide](https://getstream.io/blog/activity-feed-design/)

---

### Pattern 5: Real-Time Filtering

**Context**: Users need to narrow information streams without disrupting real-time flow.

**Implementation**:

**Filter types**:

1. **Pre-filters** (before data enters feed):
   - Source selection (which accounts/topics to follow)
   - Keyword filters (include/exclude terms)
   - Type filters (posts, replies, media only)

2. **Post-filters** (client-side, after data received):
   - Visual filtering (dim/hide but don't remove)
   - Search within stream
   - Temporary filters (session-only)

3. **Algorithmic filters** (relevance ranking):
   - Personalized feed ordering
   - Trending/popularity boosting
   - Recency weighting

**Design patterns**:

**Global filters** (apply to all streams):
- Notification importance level
- Time range (last hour, today, this week)
- Interaction type (mentions, replies, all activity)

**Per-stream filters** (override global):
- Channel-specific notification settings (Discord, Slack)
- Topic-based filtering (Reddit, Twitter)
- Saved filter views (Inoreader, Feedly)

**Visual feedback**:
- Filter pill badges showing active filters
- Item count or "X items hidden by filters"
- Temporary "show hidden" toggle
- Filter edit mode (drag to reorder priority)

**Research finding**: "A good activity stream is custom-built for the culture of its website and centers on what is relevant to the user, filtering everything else away. Algorithms analyze user activity patterns to prioritize updates most relevant to them."

**Example implementations**:

**Slack Activity view**:
- Filter by: DMs, channels, reminders, VIPs
- Custom views combining multiple filters
- Density options (compact, comfortable, spacious)
- Bulk actions on filtered results

**Feedly**:
- "More signal, less noise" philosophy
- AI-powered relevance filtering
- Saved searches as filters
- Mute specific sources temporarily

**Inoreader**:
- Permanent content storage (no time limits)
- Rules-based filtering (if-then logic)
- Regex support for power users
- Filter statistics (how many items affected)

**Sources**:
- [Smashing Magazine: UX Strategies for Real-Time Dashboards](https://www.smashingmagazine.com/2025/09/ux-strategies-real-time-dashboards/)
- [Slack: Introducing new Activity view](https://slack.com/help/articles/46751260742035-Introducing-the-new-Activity-view-in-Slack)
- [Inoreader vs Feedly comparison](https://www.inoreader.com/alternative-to-feedly)

---

### Pattern 6: Multi-Stream Layouts

**Context**: Users monitor multiple independent data sources simultaneously.

**Layout types**:

**1. Single-stream dashboard**:
- One primary data stream
- Supporting widgets/charts around edges
- Focus on depth over breadth

**2. Multi-stream dashboard**:
- Multiple independent streams (2-6 typical)
- Each stream can be different entity type
- Shared filtering across all streams

**Layout configurations**:

**Horizontal split**:
- 2-3 streams side-by-side
- Good for comparison tasks
- Desktop-oriented (wide screens)

**Vertical stack**:
- Streams stacked vertically
- Mobile-friendly
- Scroll to see more streams

**Grid layout**:
- 4-6 streams in 2x2 or 2x3 grid
- Dashboard/command-center feel
- High information density

**Tabbed streams**:
- One visible stream at a time
- Tabs for quick switching
- Lower cognitive load, less clutter

**Design considerations**:

**Visual filters** (global):
- Apply to all streams simultaneously
- Placed above streams (Dynamics 365 pattern)
- Dynamic filter options based on stream contents

**Per-stream configuration**:
- Each stream selects entity type (accounts, issues, events)
- Each stream selects view (sorting, grouping)
- Independent refresh rates possible

**Interaction patterns**:
- Click item in stream → detail panel or modal
- Drag items between streams (if supported)
- Collapse/expand streams
- Rearrange stream order

**Example: Dynamics 365 Interactive Dashboard**:
- Multi-stream with visual filters across top
- Each stream shows different entity (cases, contacts, accounts)
- Click visual filter → all streams update
- Side-by-side comparison supported

**Example: Notion Activity Log**:
- Single stream of workspace activity
- Filter by: person, page, type, date
- Click item → jump to context (page, comment, etc.)

**Sources**:
- [Dynamics 365 Interactive Dashboards](https://learn.microsoft.com/en-us/dynamics365/customerengagement/on-premises/customize/configure-interactive-experience-dashboards)
- [Carl de Souza: Single vs Multi-Stream Dashboards](https://carldesouza.com/using-creating-single-stream-multi-stream-dashboards-dynamics-365/)

---

### Pattern 7: Ambient Notifications vs Alerts

**Context**: Balancing user awareness with avoiding unwanted distraction.

**Definitions**:

**Ambient notifications**:
- Peripheral awareness without demanding attention
- Continuous or gradual changes
- Visual, auditory, or tactile cues in environment
- User absorbs information passively

**Alerts**:
- Demand immediate attention
- Discrete events (not continuous)
- Often modal (block other actions)
- User must actively respond

**Core design challenge**: "Preventing unwanted distraction to primary task while still delivering information in an accurate and timely manner."

**Ambient notification patterns**:

**1. Peripheral displays**:
- Information on edge of screen (sidebar, status bar)
- Doesn't interrupt main task
- User glances when convenient
- Example: Slack activity sidebar, GitHub notification dot

**2. Progressive obtrusiveness**:
- Starts subtle, gradually becomes more noticeable
- Gives user time to wrap up primary task
- Example: Ambient Timer (light slowly brightens before event)

**3. Continuous light patterns**:
- Color/brightness indicates state
- Slow transitions (not sudden changes)
- Example: Build status lights (green/yellow/red)

**4. Sound design**:
- Quiet ambient tones vs loud alerts
- Musical/pleasant sounds for ambient awareness
- Harsh/urgent sounds for critical alerts

**Alert patterns**:

**1. Modal interruptions**:
- Block current task
- Use sparingly (critical errors only)
- Example: "Server connection lost"

**2. Notification center**:
- Collect alerts in dedicated space
- User reviews at their convenience
- Example: macOS Notification Center, Windows Action Center

**3. Toast/snackbar**:
- Brief popup (3-5 seconds)
- Doesn't block interaction
- Auto-dismiss or user-dismiss
- Example: "Message sent", "File saved"

**4. Badge counters**:
- Numeric indicator on icon
- Persistent until user clears
- Example: Unread email count, app update badge

**Decision framework**:

| Information Type | Urgency | Recommend |
|------------------|---------|-----------|
| Build status | Low | Ambient (peripheral light) |
| New chat message | Medium | Toast notification |
| Upcoming meeting (30 min) | Medium | Ambient → alert progression |
| Server crash | High | Modal alert |
| Friend online | Low | Ambient (status indicator) |
| Payment failed | High | Alert + email |
| Background task complete | Low | Badge counter |

**User perception research**:

"Users view notifications as a mechanism to provide passive awareness rather than a trigger to switch tasks. Users acknowledge notifications as disruptive, yet opt for them because of their perceived value in providing awareness."

**Design principles**:

1. **Default to ambient** unless urgency justifies alert
2. **Progressive escalation**: Start ambient, escalate if ignored
3. **User control**: Let users set notification thresholds
4. **Context awareness**: Suppress during "focus mode" or meetings
5. **Consolidation**: Batch related notifications (not 10 separate emails)

**Sources**:
- [Material Design: Notifications](https://m1.material.io/patterns/notifications.html)
- [Toptal: Notification Design Guide](https://www.toptal.com/designers/ux/notification-design)
- [Research: Towards Ambient Notifications](https://www.researchgate.net/publication/255708939_Towards_Ambient_Notifications)
- [Carbon Design: Notification Pattern](https://carbondesignsystem.com/patterns/notification-pattern/)

---

### Pattern 8: Live Chat/Thread Interaction

**Context**: High-velocity conversation streams where messages arrive faster than users can read.

**Challenges**:

1. **Message velocity**: 10-100+ messages/minute in active chats
2. **Scroll hijacking**: New messages auto-scroll, interrupting reading
3. **Context loss**: Hard to follow conversations in chaotic stream
4. **Signal vs noise**: Important messages buried in flood

**Solutions**:

**1. Auto-scroll with pause**:
- New messages auto-scroll feed
- Scroll up manually → pause auto-scroll
- "New messages" button to jump back to live
- Prevent disorientation when reading history

**2. Threaded replies**:
- Click message → open thread
- Side conversation without main channel clutter
- Popular on Slack, Discord, Twitch
- Reduces noise in main feed

**Implementation example** (Twitch):
- Reply to message → creates thread
- Thread shown in sidebar or modal
- Main chat continues flowing
- Thread participants get notifications

**3. Slow mode**:
- Rate limit: 1 message per N seconds per user
- Reduces flood in popular streams
- Example: Twitch slow mode (3 sec, 10 sec, 30 sec options)

**4. Emote-only mode**:
- Disable text, allow only emotes/reactions
- Reduces spam while maintaining engagement
- Popular during high-hype moments

**5. Pinned messages**:
- Important messages stay at top
- Moderator/admin action
- Doesn't scroll away with new messages

**6. Subscriber/VIP priority**:
- Highlight messages from specific user groups
- Filter view to show only VIP messages
- Twitch subscriber chat badges

**Interaction rituals**:

Research finding: "Online interaction rituals rely heavily on shared symbols, knowledge, and communication patterns, which are simultaneously barriers to outsiders and substitutes for physical behavior synchronization."

**Shared symbols**:
- Emotes (custom per community)
- Copypasta (repeated message patterns)
- Call-and-response phrases

**Real-time feedback loops**:
- Streamer acknowledges subscription → chat reacts
- Parallel game events discussed in real-time
- Viewers interact with each other and streamer simultaneously

**Hybrid approaches**:

**StreamThreads** (Twitch extension):
- Reddit-style threaded discussions
- Dynamically ranked by recency + upvotes
- Users create threads without leaving stream
- Sidebar conversations persist beyond live moment

**Sources**:
- [Twitch: Chat Basics](https://link.twitch.tv/ChatBasics)
- [GetStream: Livestream Chat UX - Threads and Replies](https://getstream.io/blog/exploring-livestream-chat-ux-threads-and-replies/)
- [Research: Building viewer engagement on Twitch](https://www.tandfonline.com/doi/full/10.1080/1369118X.2021.1913211)
- [StreamThreads on Devpost](https://devpost.com/software/streamthreads)

---

### Pattern 9: Visual Indicators for Real-Time Updates

**Context**: Users need immediate feedback when data changes without reading full content.

**Animation patterns**:

**1. Color flash**:
- Brief color change on update (200-500ms)
- Green for positive change (price up, task complete)
- Red for negative change (price down, error)
- Returns to default color after flash

**Cultural consideration**: "In Western finance resources, price rise is green, drop is red. In Asian countries, everything is opposite."

**2. Smooth transitions**:
- Animate value changes (count-up/count-down)
- Users perceive the direction and magnitude of change
- Example: Stock price sliding from $100 → $105
- Easing curves make changes feel natural

**3. Pulse/glow**:
- Subtle glow around updated item
- Draws eye without demanding attention
- Fades after 1-2 seconds
- Example: New notification in sidebar

**4. Bold/unbold toggle**:
- New/unread items in bold
- Read items in regular weight
- Simple, accessible, no color dependency

**5. Badges and dots**:
- Small colored circle on icon
- Indicates presence of new content
- Example: Red notification dot on app icon

**Implementation considerations**:

**Performance**:
- CSS transitions/animations preferred over JavaScript
- GPU-accelerated properties (transform, opacity)
- Debounce rapid updates to prevent animation stutter
- WebGL for complex visualizations (TradingView charts)

**Accessibility**:
- Don't rely solely on color (use shape, text, icons)
- Support reduced-motion preferences
- Screen reader announcements for updates
- Keyboard navigation for interactive elements

**Real-time data architecture**:

**WebSocket pattern**:
```javascript
// Server pushes updates
socket.on('price_update', (data) => {
  updatePrice(data.symbol, data.price);
  flashColor(data.symbol, data.price > oldPrice ? 'green' : 'red');
});
```

**Polling pattern** (fallback):
```javascript
// Client requests updates periodically
setInterval(() => {
  fetch('/api/prices')
    .then(data => updatePrices(data));
}, 5000); // Every 5 seconds
```

**Server-Sent Events** (SSE):
```javascript
// Server streams updates
const eventSource = new EventSource('/api/stream');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateFeed(data);
};
```

**Chart animation benefits**:

Research finding: "Animated charts help viewers see data patterns unfold in real time. When viewers watch the data move, they understand the story without needing a finance degree."

**Example: TradingView**:
- JavaScript + WebGL for fast rendering
- Hybrid server/client rendering
- Preloading and caching reduce latency
- Feels "close to native" despite being web-based

**Sources**:
- [PixelFree Studio: Real-Time Stock Tickers](https://blog.pixelfreestudio.com/how-to-implement-real-time-stock-tickers-in-web-applications/)
- [TechSpective: Tech Behind Real-Time Charts](https://techspective.net/2025/05/06/the-tech-behind-real-time-chart-generation-in-metatrader-and-tradingview/)
- [Syncfusion: React Stock Chart Libraries 2026](https://www.syncfusion.com/blogs/post/top-5-react-stock-charts-in-2026)

---

## Architecture Patterns

### Push vs Pull Feed Models

**Pull Model** (on-demand generation):

**How it works**:
- User opens app → timeline generated in real-time
- Query: "Get posts from everyone I follow, sorted by recency/algorithm"
- Content ranked on-the-fly

**Pros**:
- Always up-to-date
- No stale pre-computed feeds
- Easier to implement initially
- Less storage (no cached timelines)

**Cons**:
- Slow for users with many follows
- High database load
- Latency spikes during peak traffic

**Best for**:
- Small user bases
- Infrequent updates
- When personalization changes often

**Push Model** (pre-computed timelines):

**How it works**:
- New post created → immediately pushed to all followers' timelines
- Pre-compute and cache timelines
- User opens app → instant load from cache

**Pros**:
- Fast timeline loads (already computed)
- Low latency for end users
- Scales better for read-heavy workloads

**Cons**:
- Stale feeds (pre-computed may be outdated)
- High write amplification (1 post → N follower updates)
- Complex to implement
- Storage intensive (cached timelines per user)

**Best for**:
- Large user bases (Twitter, Instagram scale)
- Read-heavy usage (10:1 read:write ratio)
- When speed is critical

**Hybrid approaches**:

- **Fanout on write** for users with <N followers (push)
- **Fanout on read** for celebrity accounts (pull)
- Smart caching strategies (Redis, Memcached)
- Event-driven architecture (Kafka, AWS Kinesis)

**Real-time considerations**:

"Backend systems use event-driven architecture to process updates instantly, with queueing engines like Kafka or AWS Kinesis ensuring low-latency event streaming."

**Sources**:
- [DEV: Designing News Feed Systems](https://dev.to/sgchris/designing-a-news-feed-system-facebook-and-twitter-architecture-5292)
- [GetStream: Activity Feeds 101](https://getstream.io/blog/activity-feeds-101/)

---

## Discovery vs Monitoring: Pattern Selection

### Discovery Use Case

**User goal**: Explore content, find interesting items, spend time browsing.

**Recommended patterns**:
- ✅ Infinite scroll (minimize friction)
- ✅ Algorithmic filtering (surface relevant content)
- ✅ Rich media previews (images, videos inline)
- ✅ Read/unread tracking (remember what was seen)
- ✅ Save for later / bookmarking
- ✅ Related content suggestions
- ❌ Speed controls (not needed, user scrolls at own pace)
- ❌ Real-time updates (can wait, not time-sensitive)

**Example applications**:
- Twitter/X feed
- Instagram Explore
- Reddit front page
- YouTube recommendations
- Pinterest boards

### Monitoring Use Case

**User goal**: Stay aware of changes, react to important events, minimize time spent.

**Recommended patterns**:
- ✅ Pause/resume controls (critical for real-time)
- ✅ Speed controls (adjust to cognitive load)
- ✅ Ambient notifications (peripheral awareness)
- ✅ Visual update indicators (flash, color, bold)
- ✅ Filtering by importance/type
- ✅ Multi-stream layouts (monitor multiple sources)
- ❌ Infinite scroll (need landmarks, completion)
- ❌ Rich media (distracting, slows scanning)

**Example applications**:
- Stock tickers (TradingView)
- Server monitoring dashboards
- GitHub/Linear issue feeds
- Slack activity view
- Live sports scores

### Hybrid Use Case

**User goal**: Both discover new content AND monitor specific streams.

**Recommended patterns**:
- ✅ Tabbed interface (switch between modes)
- ✅ Notification center (collect alerts separately)
- ✅ Customizable views (save filter configurations)
- ✅ VIP/priority lists (important items surface)
- ✅ Multi-stream with density controls

**Example applications**:
- Discord (channels + activity feed)
- Notion (content + activity log)
- Feedly (reading mode + monitoring mode)

---

## Implementation Checklist

When designing an interactive feed, consider:

### Required Features (All Feeds)
- [ ] Clear visual hierarchy (what's most important?)
- [ ] Loading states (skeleton screens, spinners)
- [ ] Error states (network failure, no results)
- [ ] Empty states (new user, all filtered out)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Keyboard navigation (accessibility)
- [ ] Screen reader support (ARIA labels)

### Real-Time Features
- [ ] Pause/resume controls (if auto-updating)
- [ ] "Jump to latest" button (if paused)
- [ ] Visual indicators for updates (flash, badge)
- [ ] Stale data warnings (if paused too long)
- [ ] Connection status indicator (WebSocket connected?)

### Filtering & Search
- [ ] Global filters (apply to all content)
- [ ] Per-stream filters (if multi-stream)
- [ ] Search within feed
- [ ] Saved filter views
- [ ] Filter clear/reset

### State Management
- [ ] Read/unread tracking
- [ ] Cross-device sync
- [ ] Mark as read/unread actions
- [ ] Archive/hide functionality
- [ ] Bulk actions (select multiple)

### Performance
- [ ] Virtualized scrolling (for long lists)
- [ ] Lazy loading images
- [ ] Debounced updates (prevent thrashing)
- [ ] Optimistic UI updates (instant feedback)
- [ ] Offline support (cache recent data)

### Notifications
- [ ] In-app notifications (toasts, badges)
- [ ] Push notifications (mobile, desktop)
- [ ] Email digests (optional)
- [ ] Notification preferences (per-channel, per-type)
- [ ] Do Not Disturb mode

---

## Research Citations

All sources are listed within individual pattern sections above. Key research themes:

1. **Accessibility**: WCAG 2.2.2 requirements for pause/stop/hide controls
2. **User behavior**: Infinite scroll encourages continuous attention, pagination supports goal-oriented tasks
3. **Cognitive load**: Interruptions trigger task-switching, ambient notifications preserve focus
4. **Real-time architecture**: Event-driven systems with Kafka/Kinesis for low latency
5. **Cultural considerations**: Color semantics vary (green/red meanings differ globally)
6. **Engagement patterns**: Shared symbols and interaction rituals build community (Twitch research)

---

## Conclusion

Interactive ticker and feed design is not one-size-fits-all. The most successful implementations:

1. **Match patterns to user intent**: Discovery vs monitoring require different approaches
2. **Respect cognitive limits**: Ambient awareness beats constant interruption
3. **Provide user control**: Pause, speed, filters, notification preferences
4. **Design for real-time**: WebSockets, event streams, optimistic UI
5. **Consider accessibility**: Keyboard nav, screen readers, reduced motion
6. **Test with users**: Interaction patterns feel different at scale

The pattern library above provides a foundation. Adapt to your specific domain, user needs, and technical constraints.

---

**Document status**: Research synthesis
**Author**: Rowan Valle
**Date**: 2026-02-07
**Domains**: UX, patterns, real-time, interaction-design
**Next steps**: Test patterns in prototype, measure engagement metrics, iterate based on user feedback
