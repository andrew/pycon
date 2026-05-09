# Zizmor scan report

- Packages fetched from proxy.golang.org: 644
  - No repo URL: 81
  - github.com: 554
  - cs.opensource.google: 6
  - gitlab.com: 1
  - go.googlesource.com: 1
  - dmitri.shuralyov.com: 1
- Packages with GitHub repos: 554 (515 unique repos)
- Repos scanned: 311
- Repos without workflows: 0 (0.0%)
- Repos with findings: 309 (99.4%)
- Total findings: 4214
  - High: 261 repos (83.9%)
  - Medium: 299 repos (96.1%)
  - Low: 59 repos (19.0%)
  - Informational: 15 repos (4.8%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/Azure/go-autorest | 11 |
| https://github.com/aws/aws-sdk-go-v2 | 7 |
| https://github.com/etcd-io/etcd | 4 |
| https://github.com/urfave/cli | 2 |
| https://github.com/ugorji/go | 2 |
| https://github.com/russross/blackfriday | 2 |
| https://github.com/pelletier/go-toml | 2 |
| https://github.com/onsi/ginkgo | 2 |
| https://github.com/klauspost/cpuid | 2 |
| https://github.com/jmespath/go-jmespath | 2 |
| https://github.com/jackc/pgproto3 | 2 |
| https://github.com/jackc/chunkreader | 2 |
| https://github.com/hashicorp/consul | 2 |
| https://github.com/googleapis/gax-go | 2 |
| https://github.com/google/martian | 2 |
| https://github.com/golang-jwt/jwt | 2 |
| https://github.com/godbus/dbus | 2 |
| https://github.com/go-gl/glfw | 2 |
| https://github.com/cpuguy83/go-md2man | 2 |
| https://github.com/coreos/go-systemd | 2 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| artipacked | Medium | 290 | 93.2% | 986 |
| unpinned-uses | High | 250 | 80.4% | 1613 |
| excessive-permissions | Medium | 219 | 70.4% | 674 |
| secrets-outside-env | Medium | 50 | 16.1% | 214 |
| cache-poisoning | High | 40 | 12.9% | 107 |
| dangerous-triggers | High | 26 | 8.4% | 33 |
| template-injection | Low | 25 | 8.0% | 465 |
| secrets-inherit | Medium | 19 | 6.1% | 93 |
| superfluous-actions | Low | 7 | 2.3% | 12 |
| unpinned-images | High | 3 | 1.0% | 6 |
| archived-uses | Medium | 2 | 0.6% | 2 |
| bot-conditions | High | 2 | 0.6% | 2 |
| use-trusted-publishing | Informational | 2 | 0.6% | 3 |
| github-env | High | 1 | 0.3% | 2 |
| misfeature | Low | 1 | 0.3% | 1 |
| unsound-condition | High | 1 | 0.3% | 1 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| Medium | 299 | 96.1% | 1746 |
| High | 261 | 83.9% | 1828 |
| Low | 59 | 19.0% | 565 |
| Informational | 15 | 4.8% | 75 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/google/flatbuffers | 9 | 137 | 4010 |
| https://github.com/envoyproxy/protoc-gen-validate | 8 | 63 | 4649 |
| https://github.com/hashicorp/consul | 7 | 658 | 7828 |
| https://github.com/cyphar/filepath-securejoin | 7 | 56 | 5997 |
| https://github.com/pact-foundation/pact-go | 7 | 38 | 141 |
| https://github.com/nats-io/nats-server | 6 | 89 | 6417 |
| https://github.com/grpc-ecosystem/grpc-gateway | 6 | 22 | 16226 |
| https://github.com/Shopify/logrus-bugsnag | 6 | 15 | 356 |
| https://github.com/Shopify/toxiproxy | 6 | 15 | 890 |
| https://github.com/prometheus/client_golang | 6 | 11 | 36473 |
| https://github.com/containerd/containerd | 5 | 148 | 9153 |
| https://github.com/docker/docker | 5 | 98 | 16935 |
| https://github.com/apache/thrift | 5 | 91 | 3732 |
| https://github.com/cilium/ebpf | 5 | 50 | 1753 |
| https://github.com/pelletier/go-toml | 5 | 38 | 26833 |
| https://github.com/gopherjs/gopherjs | 5 | 35 | 10100 |
| https://github.com/casbin/casbin | 5 | 32 | 1633 |
| https://github.com/bketelsen/crypt | 5 | 24 | 318 |
| https://github.com/docker/docker-credential-helpers | 5 | 23 | 5004 |
| https://github.com/coreos/bbolt | 5 | 22 | 7187 |

## High severity (excluding unpinned-uses)

215 findings across 65 repos (20.9%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| cache-poisoning | 40 | 107 |
| dangerous-triggers | 26 | 33 |
| template-injection | 11 | 64 |
| unpinned-images | 3 | 6 |
| bot-conditions | 2 | 2 |
| unsound-condition | 1 | 1 |
| github-env | 1 | 2 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/hashicorp/consul | 3 | 43 | 7828 |
| https://github.com/Azure/azure-sdk-for-go | 3 | 12 | 10104 |
| https://github.com/grpc-ecosystem/grpc-gateway | 3 | 7 | 16226 |
| https://github.com/envoyproxy/protoc-gen-validate | 3 | 5 | 4649 |
| https://github.com/nats-io/nats-server | 3 | 3 | 6417 |
| https://github.com/docker/docker | 2 | 11 | 16935 |
| https://github.com/Shopify/logrus-bugsnag | 2 | 5 | 356 |
| https://github.com/coreos/bbolt | 2 | 4 | 7187 |
| https://github.com/google/flatbuffers | 2 | 4 | 4010 |
| https://github.com/pact-foundation/pact-go | 2 | 4 | 141 |
| https://github.com/Shopify/toxiproxy | 2 | 3 | 890 |
| https://github.com/envoyproxy/go-control-plane | 2 | 2 | 7382 |
| https://github.com/pelletier/go-toml | 2 | 2 | 26833 |
| https://github.com/prometheus/client_golang | 2 | 2 | 36473 |
| https://github.com/containerd/containerd | 1 | 12 | 9153 |
| https://github.com/opencontainers/runc | 1 | 8 | 7425 |
| https://github.com/containerd/cgroups | 1 | 6 | 5218 |
| https://github.com/cyphar/filepath-securejoin | 1 | 6 | 5997 |
| https://github.com/bketelsen/crypt | 1 | 5 | 318 |
| https://github.com/opencontainers/selinux | 1 | 4 | 1881 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/hashicorp/consul | 4000 | 7 | 658 | 7828 |
| https://github.com/google/flatbuffers | 1176 | 9 | 137 | 4010 |
| https://github.com/containerd/containerd | 895 | 5 | 148 | 9153 |
| https://github.com/apache/thrift | 883 | 5 | 91 | 3732 |
| https://github.com/nats-io/nats-server | 770 | 6 | 89 | 6417 |
| https://github.com/docker/docker | 570 | 5 | 98 | 16935 |
| https://github.com/envoyproxy/protoc-gen-validate | 538 | 8 | 63 | 4649 |
| https://github.com/opencontainers/runc | 488 | 3 | 61 | 7425 |
| https://github.com/cyphar/filepath-securejoin | 457 | 7 | 56 | 5997 |
| https://github.com/cilium/ebpf | 434 | 5 | 50 | 1753 |
| https://github.com/fsnotify/fsnotify | 337 | 4 | 41 | 60404 |
| https://github.com/googleapis/google-cloud-go | 336 | 3 | 39 | 14312 |
| https://github.com/pelletier/go-toml | 334 | 5 | 38 | 26833 |
| https://github.com/Microsoft/hcsshim | 328 | 4 | 42 | 4104 |
| https://github.com/pact-foundation/pact-go | 323 | 7 | 38 | 141 |
| https://github.com/go-redis/redis | 303 | 4 | 34 | 5536 |
| https://github.com/gin-contrib/sse | 298 | 4 | 32 | 22995 |
| https://github.com/aws/aws-sdk-go-v2 | 286 | 4 | 32 | 9859 |
| https://github.com/otiai10/copy | 276 | 3 | 33 | 2899 |
| https://github.com/gopherjs/gopherjs | 275 | 5 | 35 | 10100 |
| https://github.com/opencontainers/selinux | 262 | 4 | 34 | 1881 |
| https://github.com/casbin/casbin | 259 | 5 | 32 | 1633 |
| https://github.com/checkpoint-restore/go-criu | 243 | 4 | 28 | 462 |
| https://github.com/containerd/cgroups | 238 | 4 | 31 | 5218 |
| https://github.com/gin-gonic/gin | 218 | 3 | 23 | 30041 |
| https://github.com/docker/docker-credential-helpers | 216 | 5 | 23 | 5004 |
| https://github.com/lib/pq | 202 | 3 | 24 | 27676 |
| https://github.com/Azure/azure-sdk-for-go | 201 | 5 | 20 | 10104 |
| https://github.com/kubernetes/utils | 198 | 3 | 24 | 20971 |
| https://github.com/goccy/go-json | 195 | 4 | 24 | 18737 |
