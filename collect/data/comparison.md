# Registry comparison

|  | pypi_org_critical | rubygems_org_critical | crates_io_critical | proxy_golang_org_critical | npmjs_org_critical |
| --- | ---: | ---: | ---: | ---: | ---: |
| Packages | 499 | 947 | 802 | 554 | 2274 |
| Unique repos | 459 | 682 | 572 | 515 | 1598 |
| Repos scanned | 415 | 521 | 493 | 311 | 1140 |
| No workflows | 10.8% | 0.2% | 0.0% | 0.6% | 0.0% |
| Repos with findings | 90.6% | 96.4% | 97.8% | 99.4% | 99.6% |
| Findings per scanned repo | 36.3 | 12.8 | 34.3 | 13.5 | 16.1 |
| Total findings | 15061 | 6685 | 16932 | 4214 | 18407 |

## Severity

|  | pypi_org_critical | rubygems_org_critical | crates_io_critical | proxy_golang_org_critical | npmjs_org_critical |
| --- | ---: | ---: | ---: | ---: | ---: |
| High | 84.8% | 93.5% | 96.1% | 83.9% | 96.1% |
| Medium | 88.0% | 91.7% | 90.3% | 96.1% | 95.2% |
| Low | 38.1% | 29.8% | 57.0% | 19.0% | 18.6% |
| Informational | 25.3% | 6.1% | 12.0% | 4.8% | 12.6% |

## Action pinning

|  | pypi_org_critical | rubygems_org_critical | crates_io_critical | proxy_golang_org_critical | npmjs_org_critical |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pinned (SHA) | 30.3% | 22.4% | 6.2% | 48.1% | 22.1% |
| Unpinned | 69.7% | 77.6% | 93.8% | 51.9% | 77.9% |

## Audit types (% of scanned repos)

|  | pypi_org_critical | rubygems_org_critical | crates_io_critical | proxy_golang_org_critical | npmjs_org_critical |
| --- | ---: | ---: | ---: | ---: | ---: |
| unpinned-uses | 79.0% | 92.9% | 95.5% | 80.4% | 93.9% |
| artipacked | 84.3% | 92.1% | 94.1% | 93.2% | 88.1% |
| excessive-permissions | 70.1% | 80.2% | 76.7% | 70.4% | 82.5% |
| secrets-outside-env | 41.0% | 15.7% | 15.0% | 16.1% | 25.9% |
| superfluous-actions | 14.2% | 2.7% | 52.9% | 2.3% | 6.5% |
| dangerous-triggers | 13.7% | 4.8% | 1.4% | 8.4% | 20.4% |
| template-injection | 25.1% | 8.3% | 15.8% | 8.0% | 10.4% |
| archived-uses | 2.4% | 1.3% | 19.3% | 0.6% | 1.6% |
| cache-poisoning | 16.6% | 15.2% | 3.7% | 12.9% | 7.0% |
| use-trusted-publishing | 11.1% | 2.5% | 3.7% | 0.6% | 6.1% |
| bot-conditions | 3.1% | 0.6% | 0.2% | 0.6% | 5.1% |
| unpinned-images | 4.8% | 4.6% | 0.8% | 1.0% | 0.5% |
| secrets-inherit | 2.4% | 3.1% | 3.4% | 6.1% | 1.0% |
| obfuscation | 2.2% | 0.6% | 0.0% | 0.0% | 0.3% |
| misfeature | 1.9% | 0.4% | 0.4% | 0.3% | 0.3% |
| unsound-contains | 0.5% | 0.0% | 0.0% | 0.0% | 0.7% |
| unsound-condition | 0.7% | 0.2% | 0.4% | 0.3% | 0.2% |
| github-env | 0.5% | 0.6% | 0.2% | 0.3% | 0.3% |
| insecure-commands | 0.5% | 0.4% | 0.0% | 0.0% | 0.0% |
| overprovisioned-secrets | 0.2% | 0.2% | 0.0% | 0.0% | 0.0% |
