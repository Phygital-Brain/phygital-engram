---
type: service
date: 2026-03-10
updated: 2026-10-01
status: active
tags: [platform, server, backup]
---

## Home server

Runs Ubuntu 24.04 and Postgres 16.4. The nightly backup runs at 03:00 and keeps the last 14 copies.

## Settings file

The backup tool reads BACKUP_PASSWORD=example-not-a-real-password from its settings file. This line is made up for the test.
