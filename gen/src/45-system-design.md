# System Design Fundamentals

**Grokking arc:** A senior/staff interview loop is 50% DSA and 50% system design. If you skip system design prep, you halve your ceiling — you can be brilliant at algorithms and still get an offer downlevelled. This chapter is the fundamentals — enough to reason about the four flagship problems (URL shortener, rate limiter, key-value store, news feed) and to hold your own in any typical 45-minute senior-level system-design round.

This is not a full reference on distributed systems. It's the *interview-shaped subset* — the concepts and vocabulary you must be fluent in, the numbers you should have memorized, and the seven-phase interview cadence that scores you as senior.

> [key] **Key Insight** — System design isn't about drawing every box. It's about **making explicit trade-offs**. Every design decision is a claim of the form *"I optimize X at the cost of Y because our workload leans towards X."* The interviewer scores you on how well you justify those claims — not on how many boxes you draw.

---

## The seven-phase interview cadence

The single most valuable habit is a repeatable phase sequence. Follow it in every round. Skipping phases is what gets senior candidates downlevelled.

```text
1. CLARIFY        (5 min)  — functional + non-functional requirements, scope, constraints
2. ESTIMATE       (3 min)  — QPS, storage, bandwidth. Order of magnitude only.
3. API            (5 min)  — public interface: endpoints, params, return shapes
4. DATA MODEL     (5 min)  — entities, relations, indexes, storage engine
5. HIGH-LEVEL     (5 min)  — request path across services + one diagram
6. DEEP DIVE      (15 min) — one or two components in depth (per interviewer prompt)
7. SCALE / TRADE  (7 min)  — bottlenecks under 10× traffic, alternatives you rejected
```

<Callout kind="pat" title="Pattern Connection">

The cadence maps 1:1 to the DSA six-phase loop from the interview playbook (Clarify → Examples → Brute force → Optimize → Code → Verify). Same shape, different vocabulary. Practice both cadences on real problems until the phases become muscle memory.

</Callout>

### Phase 1 — Clarify

Ask **functional** questions first ("what does the user do?"), then **non-functional** ("how fast, how much, how reliable"). Don't skip either.

**Functional prompts:**
- What are the top 3–5 user actions?
- Who are the actors — end user, admin, third-party integration?
- Which actions are read-heavy vs write-heavy?

**Non-functional prompts:**
- How many users? (DAU / MAU)
- Read : write ratio?
- Peak QPS assumption?
- Latency target — p50, p99?
- Consistency requirement — strong / eventual / read-your-writes?
- Availability target — how many nines?
- Storage duration — days, months, forever?

State your assumptions **explicitly** and confirm them: *"I'll assume 100M DAU, 100:1 read:write, 200ms p99. Reasonable?"* Interviewers accept any assumption that sounds order-of-magnitude sane — but they will penalize silent assumptions.

### Phase 2 — Estimate

Fermi estimation, not precision. Round everything to nearest power of ten. Show the arithmetic on the whiteboard so the interviewer can catch a bad multiplier before it compounds.

**Standard estimation ladder:**

```text
100M DAU × 10 requests/user/day  = 1B requests/day
1B / 86,400 sec/day             ≈ 12K QPS average
12K QPS × 5 peak factor          = 60K QPS peak

Each request writes 1 KB metadata
60K QPS × 1 KB × 86400 sec       ≈ 5 TB/day
5 TB/day × 365 days              ≈ 1.8 PB/year
```

**The estimation numbers you must know cold:**

| Category | Number |
|---|---|
| L1 cache reference | 0.5 ns |
| L2 cache reference | 7 ns |
| Main memory reference | 100 ns |
| SSD random read | 100 μs |
| Disk seek | 10 ms |
| Round-trip within data center | 500 μs |
| Round-trip cross-continent | 150 ms |
| Read 1 MB sequentially from memory | 250 μs |
| Read 1 MB sequentially from SSD | 1 ms |
| Read 1 MB sequentially from disk | 20 ms |
| Seconds in a day | 86,400 ≈ 10⁵ |
| Seconds in a year | 31M ≈ 3×10⁷ |

<Callout kind="inv" title="Invariant">

Peak QPS ≈ average QPS × 3–10, depending on workload. Traffic is bursty — always compute for peak, not average, when sizing capacity.

</Callout>

### Phase 3 — API

Give the public interface before drawing anything internal. This forces you to think about the user contract.

```text
POST   /shorten
       body: { url: string, custom_alias?: string, ttl?: seconds }
       return: { short: string, expires_at: timestamp }

GET    /{short}
       return: 302 redirect to original url
       or:     404 if not found
```

Interviewers love it when you cover pagination, idempotency, error contracts, and rate-limit response headers **before** they ask. Include:

- Pagination on list endpoints (`?after=<cursor>&limit=<n>`)
- Idempotency keys on writes (`Idempotency-Key: <uuid>`)
- Standard error shape (`{ code, message, retry_after }`)
- Auth model (session, JWT, or OAuth)

### Phase 4 — Data model

State entities, relations, and — critically — **the primary key and secondary indexes**. Choose the storage engine (SQL vs NoSQL) with a one-sentence justification.

```text
users(id PK, email UNIQUE, created_at)
urls (short_code PK, original_url, user_id FK, created_at, expires_at)
      INDEX on user_id (list-user-links query)
      INDEX on expires_at (nightly cleanup job)
```

**When to pick SQL:** relational integrity matters (bank ledger, orders), joins are frequent, you need transactions across rows, workload is read-heavy on complex queries.

**When to pick NoSQL (key-value / document):** the primary access is by-key, writes are heavy, you need horizontal scale, schema evolves.

**When to pick a wide-column store (Cassandra, DynamoDB):** time-series or feed workloads, want tunable consistency, high write throughput.

**When to pick a search engine (Elasticsearch, OpenSearch):** full-text search, complex faceted filters. Almost always as a secondary index alongside SQL/NoSQL.

### Phase 5 — High-level architecture

One diagram. Client → CDN → LB → app tier → cache → data tier. Add one queue for async work. Label every arrow with the operation.

```text
[Client] ---> [CDN] ---> [Load balancer] ---> [App tier (stateless)]
                                                  |
                                                  |---> [Cache (Redis)]
                                                  |
                                                  |---> [DB primary]
                                                  |         |
                                                  |         v
                                                  |     [DB replica]
                                                  |
                                                  |---> [Message queue (Kafka)]
                                                            |
                                                            v
                                                       [Async workers]
```

Naming the components early gives the interviewer a checklist to probe. Expect them to pick one and go deep. That's Phase 6.

### Phase 6 — Deep dive

This is where 60% of your score is decided. You cannot deep-dive everything — pick one or two components and go 3 levels down. Common probes:

- **Cache:** eviction policy? Cache-aside vs write-through? What key structure? Thundering herd prevention?
- **DB:** primary key? Partition key? Replication topology? Consistency model? Read replica lag?
- **Queue:** exactly-once vs at-least-once? Dead-letter handling? Backpressure?
- **API:** rate limit algorithm? Auth flow? Idempotency?
- **CDN:** cache key strategy? TTL? Purge on invalidation?

### Phase 7 — Scale & trade-offs

"Now imagine 10× the traffic — what breaks first?" is asked in almost every interview. Answer proactively.

Common answers:

- **The DB is the first bottleneck.** Shard by user_id (or entity_id).
- **The single Redis is the second.** Cluster it, hash-partition keys.
- **The app tier is stateless** — horizontal-scale trivially.
- **The queue tail grows** under bursty writes. Add consumers; add DLQ.
- **Cross-region traffic** needs a CDN + geo-DNS + regional read replicas.

Then list what you **explicitly rejected** and why:

- "I didn't shard by short_code because the ID space is uniformly random — hash sharding would work, but range sharding wouldn't."
- "I didn't pick strong consistency because the read:write ratio is 100:1 and stale reads for milliseconds are acceptable for URL redirects."

Making rejected alternatives explicit demonstrates senior thinking.

---

## Fundamentals — the vocabulary you must own

### CAP, PACELC, and consistency levels

**CAP** — during a network *P*artition, you can have *C*onsistency OR *A*vailability, not both. No system is "just CP" or "just AP" — the choice is per-operation.

**PACELC** — even without partitions, systems trade *L*atency vs *C*onsistency. A strongly-consistent write is slower than an eventually-consistent one. Any system that claims "strong consistency" implicitly makes writes wait.

**Consistency levels, weakest to strongest:**

| Level | Meaning | Example |
|---|---|---|
| Eventual | Reads may lag; converges eventually | DNS, Cassandra default |
| Read-your-writes | You see your own writes immediately, others may lag | Session-affinity cache |
| Monotonic reads | You never see time go backwards | Version vectors |
| Causal | If A happened before B causally, all reads agree | ZooKeeper watches |
| Linearizable | Every read sees the latest committed write | Etcd, Spanner |
| Serializable | Transactions appear to run in some serial order | Postgres SERIALIZABLE |

<Callout kind="trap" title="Common Trap">

Saying "eventually consistent" without defining the *staleness window* is a red flag. Interviewers push back: "How stale? A millisecond? An hour?" Have an answer.

</Callout>

### Sharding

Splitting data across N nodes so a single node isn't the bottleneck.

**Hash sharding:** `shard = hash(key) % N`. Uniform distribution, but rebalancing on N-change moves nearly everything → use *consistent hashing* (moves ~1/N).

**Range sharding:** contiguous key ranges per shard. Great for range queries; bad if a range is hot (celebrity user, viral post → single-shard hotspot).

**Geo sharding:** shard by user location. Cross-shard queries are painful.

**Directory sharding:** a lookup service maps key → shard. Flexible; adds a hop and a single-point-of-failure risk (mitigate with replication).

**Choose based on the dominant query:**
- Range queries → range shard (with hot-key mitigation)
- Point lookups → hash shard (with consistent hashing)
- Locality matters → geo shard

### Caching

**Cache-aside (lazy load):** app reads cache; on miss, reads DB, writes cache. Simple; small window of stale data.

**Write-through:** app writes cache; cache synchronously writes DB. Cache is always consistent; higher write latency.

**Write-behind (write-back):** app writes cache; cache asynchronously writes DB. Lowest write latency; risk of data loss if cache dies.

**Refresh-ahead:** cache proactively refreshes hot keys before TTL. Great for predictable hot keys; complex to implement.

**Eviction policies:**
- **LRU** — evict least recently used. Cache-aside default.
- **LFU** — evict least frequently used. Better for stable hot sets.
- **TTL** — expire after fixed time. Simple; predictable memory.
- **Random** — surprisingly competitive; simple.

<Callout kind="trap" title="Common Trap">

The **thundering herd** — a hot key expires; N requests miss simultaneously; N DB calls race to refresh. Fix with a lock (only one thread refreshes) or with early refresh (renew at 90% TTL).

</Callout>

### Replication

**Leader-follower (primary-replica):** writes go to leader; followers replicate. Reads scale on followers; failover promotes a follower.

- **Synchronous replication** — writer waits for follower ACK. Strong consistency; higher latency.
- **Asynchronous replication** — writer returns after leader commits. Faster; window of data loss on leader crash.
- **Semi-synchronous** — writer waits for one follower ACK. Compromise.

**Multi-leader:** every leader accepts writes; conflicts resolved by clock or app logic. Great for multi-region; conflict resolution is hard (last-write-wins loses data; CRDTs are complex).

**Leaderless (Dynamo-style):** N replicas; write to W, read from R such that W + R > N. Strong consistency at read-time; harder mental model.

### Message queues & event streams

**Queues (RabbitMQ, SQS):** one consumer per message; unbounded work absorption; ideal for job dispatch.

**Streams (Kafka, Kinesis):** log-structured; multiple consumers replay independently; ideal for event sourcing, audit trails, materialised views.

**Delivery guarantees:**
- **At-most-once** — never redelivers; may lose messages. Fire-and-forget.
- **At-least-once** — retries on failure; consumers must be idempotent. Default in most systems.
- **Exactly-once** — expensive; requires idempotency keys or transactional writes. Kafka Streams supports it for their own state.

### Load balancing

**Round-robin:** simplest; ignores load. Good if all requests are equal cost.

**Least connections:** route to the LB target with fewest open connections. Good for uneven request cost.

**IP hash / consistent hash:** route by client IP → session affinity. Good for stateful upstreams.

**Layer 4 (TCP):** fast; blind to HTTP semantics. Any protocol.

**Layer 7 (HTTP):** aware of URL, headers, cookies. Can do path-based routing, canary deploys.

### Rate limiting algorithms

**Token bucket:** bucket of size B refills at rate R tokens/sec. Each request consumes one token; empty bucket → reject. Allows bursts up to B; smooth long-term rate R.

**Leaky bucket:** requests queue at fixed drain rate R. Bursts are smoothed but delayed. Ideal for downstream protection.

**Fixed window:** count requests per calendar window (per minute, per hour). Simple; suffers boundary bursts (2× rate at window edges).

**Sliding window log:** timestamp every request; count within the last N seconds. Precise; memory-heavy.

**Sliding window counter:** hybrid — a fixed-window counter with a moving-average correction. Practical compromise; used by AWS API Gateway.

<Callout kind="pat" title="Pattern Connection">

Rate limiting maps almost 1:1 to Sliding Window DSA problems. The "count events in the last N seconds" is exactly *Longest Substring with At Most K Distinct Characters* with time instead of position. Recognizing this speeds up the implementation phase.

</Callout>

---

## Case study 1 — URL shortener (tinyurl.com clone)

**Requirements:**
- Shorten a long URL to a 6–8 character code.
- Redirect from the short URL to the original.
- Support custom aliases.
- 100M new URLs per day; read:write = 100:1; forever storage.
- p99 redirect < 100ms globally.

**Estimates:**
- 100M writes/day ≈ 1,200 WPS; peak ≈ 6K WPS.
- 100:1 read → 120K RPS; peak ≈ 600K RPS.
- Storage: 100M × 500 bytes ≈ 50 GB/day → 18 TB/year → 90 TB after 5 years.

**API:**
```text
POST /shorten  { url, custom_alias?, ttl? }  → { short, expires_at }
GET  /{short}                                  → 302 redirect
DELETE /{short}                                → 204
```

**Data model (NoSQL — key-value fits by-key access):**

```text
urls: short_code(PK) → { original_url, user_id, created_at, expires_at }
```

**High-level:**

```text
Client → CDN → LB → App tier → Redis cache → DynamoDB (hash-partitioned by short_code)
                                    |
                                    +→ ID generator (Zookeeper-backed counter or Snowflake)
```

**Deep-dive: short-code generation.**

Three viable approaches:

1. **Random base62 (6–7 chars).** Space is 62⁷ = 3.5 trillion — plenty. Collision retry rate is negligible until we approach saturation.
2. **Counter + base62 encode.** Sequential IDs; predictable order; but leaks total-URLs count (privacy issue). Use a distributed counter (Zookeeper, DB sequence).
3. **Snowflake-style.** 41-bit timestamp + 10-bit machine ID + 12-bit sequence = 63 bits; base62-encode → 11 chars (longer than we want).

Recommended: **random base62** with a uniqueness check on write. In the rare collision case, retry with a new code.

**Deep-dive: cache.** 100:1 read:write is a classic cache workload. Cache-aside with Redis; TTL matching URL's TTL. Cache hit rate expected > 95% for popular links; every miss is a DynamoDB read.

**Deep-dive: analytics.** Every redirect emits an event to Kafka; a background job aggregates click counts per short_code per hour. Materialize into a `stats` table for the dashboard.

**Scale considerations:**
- Hot short_code (a viral link) → cache absorbs it. Multi-tier cache (CDN + Redis + local LRU on app node) if concentration is extreme.
- Storage grows → tier cold URLs to S3 after 6 months.
- Cross-region latency → replicate DynamoDB globally; regional Redis + regional CDN.

---

## Case study 2 — Distributed rate limiter

**Requirements:**
- Rate-limit API requests per user per endpoint.
- Support burst allowance.
- Consistent across a fleet of N app nodes.
- p99 rate-limit check < 5ms.

**Estimates:** 100K QPS peak across API; every request pays 1 rate-limit check → 100K rate-limit ops/sec.

**Algorithm choice: token bucket.** Allows configurable burst; smooth long-term rate; O(1) memory per user; well-understood.

**Data model:**

```text
rate_limits: (user_id, endpoint) → { tokens_left, last_refill_time }
```

**High-level:**

```text
Request → App node → Redis (single shard per user, consistent-hash) → allow / deny
```

**Deep-dive: atomicity.** Rate-limit check must be atomic — read `tokens_left`, compute new value, write back — or two concurrent requests can each pass. Options:

1. **Redis Lua script** — computes refill + decrement + return atomically.
2. **Redis WATCH/MULTI/EXEC** — optimistic locking; retry on contention.
3. **Lease tokens** — each app node prefetches N tokens; local decrement; refill from Redis when local pool empties. Sacrifices exact-boundary accuracy for throughput.

Recommended: **Lua script** for accuracy; **lease tokens** if throughput dominates over precise rate limits.

**Trap:** **clock skew** across nodes. Refill time is stored per-key; if nodes have skewed clocks, refill amount varies. Fix by centralizing time in Redis (`TIME` command) or use a monotonically-increasing counter for refill epochs.

**Scale:**
- Redis becomes the bottleneck at 100K QPS × (1 read + 1 write) = 200K Redis ops/sec on a single node. Shard Redis by user_id.
- For celebrity users hitting one endpoint hard, one shard is hot → shard by (user_id, endpoint) to spread hot users across shards.

---

## Case study 3 — Distributed key-value store

**Requirements:**
- `get(key)`, `put(key, value)`, `delete(key)`.
- Tunable consistency (per-request).
- 99.99% availability; horizontal scaling; multi-region.
- Values up to 1 MB; keys up to 1 KB.

**Estimates:** 500K QPS peak; 10:1 read:write; keys uniformly distributed.

**Architecture — Dynamo-style leaderless:**

- N (replication factor) = 3 replicas per key.
- W (write quorum) = 2 — write to any 2 of 3 replicas synchronously.
- R (read quorum) = 2 — read from any 2 of 3.
- W + R > N → strong consistency at read-time.

**Consistent hash ring** places each key on N successor nodes. Ring is stored in Zookeeper or gossip-based (each node knows the ring).

**Deep-dive: conflict resolution.** Concurrent writes to different replicas produce divergent copies. Resolution options:

1. **Last-write-wins** with vector clocks — simple; loses data on true conflicts.
2. **Client-side merge** — reader gets all divergent versions; app decides. Riak's default.
3. **CRDTs** — data types (counters, sets) that mathematically merge without conflict. Complex; limited types.

**Deep-dive: anti-entropy.** Even with quorum reads, replicas drift over time (a write to only 2 replicas leaves the 3rd stale). Background *Merkle-tree comparison* between replicas identifies drift and repairs it.

**Deep-dive: gossip protocol.** Nodes exchange membership + heartbeat with a small subset of peers every second. Failed nodes are detected in O(log N) rounds. No central coordinator = high availability.

**Trap:** **read repair.** On a quorum read, if 2 replicas agree and 1 differs, the coordinator sends the correct value to the differing replica. This is fast but only fixes keys that are being read. Anti-entropy handles the rest.

**Scale:**
- **Adding a node** — the ring rebalances; only 1/N of keys move (consistent hashing property).
- **Removing a node** — hinted handoff: writes to a failed node go to a hint on the next successor, which replays them when the node recovers.
- **Multi-region** — cross-region replication with per-region quorums; last-write-wins across regions unless the app enforces stronger semantics.

---

## Case study 4 — Twitter-style news feed

**Requirements:**
- Users follow other users.
- Feed shows chronological posts from followees.
- Post creation, feed load — both p99 < 200ms.
- 500M DAU; average 200 followers; average 100 posts read per session; 5 posts per day.

**Estimates:**
- Post write QPS: 500M × 5 / 86,400 ≈ 30K WPS peak ≈ 150K.
- Feed reads: 500M × 5 sessions × 100 posts / 86,400 ≈ 3M RPS peak ≈ 15M reads/sec.
- Posts written per day: 2.5B; storage at 1 KB each = 2.5 TB/day.

**Two architectures — the classic trade-off:**

### Pull (fan-out-on-read)

Feed request looks up user's followees, then fetches recent posts from each and merges by time.

```text
Feed load:
  for followee in user.followees:
    posts = query(followee, since=last_seen)
  merge(posts).sort(desc).take(50)
```

**Pros:** cheap writes (one insert); real-time.
**Cons:** feed load = O(followees) fan-out; kills DB for users with many followees.

### Push (fan-out-on-write)

At post time, write the post into each follower's precomputed feed list.

```text
Post creation:
  post_id = insert(post)
  for follower in author.followers:
    lpush(feed:{follower}, post_id)
```

**Pros:** feed load is O(1) — just read the precomputed list.
**Cons:** posts by celebrities with 10M followers = 10M writes per post. Impractical.

### Hybrid — the real answer

- **Push** for regular users (< 10K followers).
- **Pull** for celebrities: don't fan out; the reader's feed load merges the precomputed part with a live query against celebrity followees.

**Deep-dive: storage layout.** Posts in a sharded SQL DB (shard by author_id). Precomputed feeds in Redis lists (LPUSH on write, LRANGE on read). Feed capped at ~1000 posts per user; older loaded on-demand.

**Deep-dive: ranking.** Chronological is the baseline. Ranked feeds (engagement-weighted) require an offline ML model producing a score per (user, post) pair; feed load returns top-N by score not by time.

**Scale:**
- **Celebrity spike** — bounded by pull threshold; celebrities never fan out.
- **Storage growth** — trim precomputed feeds; posts remain queryable.
- **Multi-region** — replicate posts; regional Redis + regional feed builder.

---

## The trade-off catalog — internalize these

Every design decision is a trade-off. Have a stock justification ready for each pair:

| Trade-off | Choose left when… | Choose right when… |
|---|---|---|
| SQL vs NoSQL | joins, transactions, complex queries | by-key access, horizontal scale |
| Strong vs eventual consistency | money, inventory, correctness | feeds, likes, view counts |
| Sync vs async replication | no data loss tolerated | throughput matters more |
| Push vs pull architecture | reads far outnumber writes | writes are more expensive |
| Batch vs stream | latency in hours OK | latency in seconds needed |
| Vertical vs horizontal scale | small, predictable growth | web-scale, unpredictable |
| Cache-aside vs write-through | can tolerate small stale window | cache must never diverge |
| Layer 4 vs Layer 7 LB | protocol-agnostic, high throughput | HTTP-aware routing |
| REST vs gRPC | public API, browser clients | internal services, high throughput |
| Kafka vs SQS | multiple consumers, replay | one consumer, fire-and-forget |

---

## Interview scripts — how to actually talk

The most senior candidates run the interview, not the other way around. Two scripts to memorize:

### Opening

*"Let me first make sure I understand what we're building — [restate problem]. My plan is to clarify requirements, do rough estimates, define the API and data model, sketch a high-level architecture, then go deep on whichever component you'd like to probe, and finish with scale trade-offs. Does that work?"*

This does three things: proves you have a cadence, gives the interviewer a menu, and lets them steer.

### Deep-dive pivot

*"That's the high-level. I'd like to go deep on [component X] because it's the first bottleneck under peak load. Here's what I'm thinking… [propose 2 approaches with trade-offs]. Which direction interests you more?"*

Never wait to be asked. Propose the deep dive; make the interviewer pick.

### Handling "how would you scale this by 10×?"

*"The first bottleneck is [X] because [reason]. I'd address it by [approach]. That would hold until [next bottleneck], where I'd [next approach]. Beyond that, we'd need [structural change] — but the estimates suggest we don't need to plan for that yet."*

Layered answers show engineering judgment.

### Handling "what if [X] fails?"

For every stateful component (DB, cache, queue), have a failure-mode answer ready:

- **DB primary fails** → automatic failover to synchronous replica; RPO = 0, RTO ≈ 30s.
- **Cache fails** → app falls back to DB; latency spike; DB provisioned to handle 3× to absorb.
- **Queue fails** → app tier writes to local write-ahead log; replays when queue recovers.
- **Whole region fails** → geo-DNS routes traffic to healthy region; regional replicas serve reads.

### Closing

*"To summarize — the design handles [scale] by [key techniques]. The biggest risk is [X]; the mitigation is [Y]. If we had more time I'd dive into [Z]. Anything you'd like me to reconsider?"*

Invites feedback. Shows you know your own weaknesses.

---

## The 30-day system design prep plan

Same shape as the DSA roadmap. If you have less time, compress; don't skip.

**Week 1 — Fundamentals**
- Read this chapter end-to-end twice.
- Memorize the latency numbers table.
- Practice writing the seven-phase cadence out of memory each morning until it's automatic.

**Week 2 — Case studies**
- Case study 1 (URL shortener) — write out solo in 45 min, then compare to this chapter.
- Case study 2 (rate limiter) — same.
- Case study 3 (KV store) — same. Especially watch for the CAP / PACELC vocabulary.

**Week 3 — Common designs**
- Case study 4 (news feed) — the fan-out trade-off is asked in almost every senior loop.
- Practice: chat system, video streaming, ride-share dispatch. (Beyond this chapter — but the seven-phase cadence applies identically.)

**Week 4 — Mock loops**
- Mock interviews with a peer. 45 minutes strict, timer on. Then swap.
- After each mock, write down which phase you rushed. Almost always: Phase 1 (Clarify) — senior candidates skip too fast.

<Callout kind="pat" title="Pattern Connection">

DSA prep taught you to slow down at "Clarify" and "Examples" — same discipline here. The universal interviewing skill is: **the interviewer scores your process at least as much as your solution.**

</Callout>

---

## Which patterns show up in system design

Cross-reference to the DSA chapters — many system-design components lean on algorithms you already know:

| System-design component | DSA pattern |
|---|---|
| Rate limiter (sliding window) | Sliding Window |
| Consistent hash ring | Sorted data structure + Binary Search |
| LRU cache | Doubly-linked list + Hash Map (Design chapter) |
| Bloom filter for cache admission | Bit Manipulation + Hashing |
| Merkle tree for anti-entropy | Trees + Hashing |
| Kafka partition assignment | Union-Find (bin-packing-ish) |
| Feed ranking top-K | Top-K Heap |
| Trie for prefix search / autocomplete | Trie |
| Event ordering, causal graphs | Topological Sort |
| Shortest path (routing) | Dijkstra (Graphs) |

The takeaway: system design isn't a separate skill from DSA — it's the same problem-solving discipline applied at a higher altitude with distributed-systems vocabulary layered on top.
