# Security Patch - February 19, 2026

## Overview

This security patch addresses multiple vulnerabilities identified in project dependencies.

## Latest Update (v0.1.2)

### Pillow (10.3.0 → 12.1.1)

**CVE Issues:**
- **Out-of-Bounds Write**: Memory corruption when loading PSD images
  - Affected: ≥ 10.3.0, < 12.1.1
  - Fixed in: 12.1.1

**Impact**: HIGH
**Action**: Updated to 12.1.1

---

## Previous Fixes (v0.1.1)

## Vulnerabilities Fixed

### 1. aiohttp (3.9.1 → 3.13.3)

**CVE Issues:**
- **Zip Bomb Vulnerability**: HTTP Parser auto_decompress feature vulnerable to zip bomb attacks
  - Affected: ≤ 3.13.2
  - Fixed in: 3.13.3
  
- **Denial of Service**: Vulnerability when parsing malformed POST requests
  - Affected: < 3.9.4
  - Fixed in: 3.9.4
  
- **Directory Traversal**: Path traversal vulnerability
  - Affected: ≥ 1.0.5, < 3.9.2
  - Fixed in: 3.9.2

**Impact**: HIGH
**Action**: Updated to 3.13.3 (latest patched version covering all vulnerabilities)

---

### 2. fastapi (0.104.1 → 0.109.1)

**CVE Issues:**
- **Content-Type Header ReDoS**: Regular expression denial of service vulnerability
  - Affected: ≤ 0.109.0
  - Fixed in: 0.109.1

**Impact**: MEDIUM
**Action**: Updated to 0.109.1

---

### 3. Pillow (10.1.0 → 10.3.0)

**CVE Issues:**
- **Buffer Overflow**: Memory corruption vulnerability in image processing
  - Affected: < 10.3.0
  - Fixed in: 10.3.0

**Impact**: HIGH
**Action**: Updated to 10.3.0

---

### 4. python-multipart (0.0.6 → 0.0.22)

**CVE Issues:**
- **Arbitrary File Write**: File write vulnerability via non-default configuration
  - Affected: < 0.0.22
  - Fixed in: 0.0.22
  
- **Denial of Service**: DoS via malformed multipart/form-data boundary
  - Affected: < 0.0.18
  - Fixed in: 0.0.18
  
- **Content-Type Header ReDoS**: Regular expression denial of service
  - Affected: ≤ 0.0.6
  - Fixed in: 0.0.7

**Impact**: HIGH
**Action**: Updated to 0.0.22 (latest patched version covering all vulnerabilities)

---

## Summary

| Package | Old Version | Current Version | Vulnerabilities Fixed |
|---------|-------------|-----------------|----------------------|
| aiohttp | 3.9.1 | 3.13.3 | 3 (zip bomb, DoS, directory traversal) |
| fastapi | 0.104.1 | 0.109.1 | 1 (ReDoS) |
| Pillow | 10.1.0 | 12.1.1 | 2 (buffer overflow, out-of-bounds write) |
| python-multipart | 0.0.6 | 0.0.22 | 3 (file write, DoS, ReDoS) |

**Total Vulnerabilities Fixed**: 9

---

## Verification

To verify the patches are applied:

```bash
# Check installed versions
pip list | grep -E "aiohttp|fastapi|Pillow|python-multipart"

# Expected output:
# aiohttp              3.13.3
# fastapi              0.109.1
# Pillow               12.1.1
# python-multipart     0.0.22
```

## Installation

For new installations:
```bash
pip install -r requirements.txt
```

For existing installations:
```bash
pip install --upgrade -r requirements.txt
```

## Testing

All existing tests continue to pass with updated dependencies:
```bash
pytest tests/ -v
```

## Compatibility

These updates maintain backward compatibility with existing KimiClaw code. No code changes required.

---

## Security Scan Results

- ✅ **v0.1.0**: 8 vulnerabilities (4 HIGH, 4 MEDIUM)
- ✅ **v0.1.1**: 0 vulnerabilities (8 fixed)
- ⚠️  **v0.1.1**: 1 new vulnerability discovered (Pillow PSD)
- ✅ **v0.1.2**: 0 vulnerabilities (9 total fixed)

---

**Patch Date**: February 19, 2026
**Latest Version**: v0.1.2
**Severity**: HIGH (immediate update recommended)
**Status**: ✅ Applied and Verified
**Total Vulnerabilities Fixed**: 9
