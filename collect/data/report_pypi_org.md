# Zizmor scan report: pypi.org

- Packages fetched from pypi.org: 533073
  - No repo URL: 159358
  - github.com: 362900
  - gitlab.com: 7299
  - bitbucket.org: 3510
  - codeberg.org: 4
  - generat0r.cc: 1
  - xxx.org: 1
- Packages with GitHub repos: 362899 (323202 unique repos)
- Repos scanned: 119118
- Repos without workflows: 5889 (4.9%)
- Repos with findings: 117761 (98.9%)
- Total findings: 2435417
  - High: 116766 repos (98.0%)
  - Medium: 116296 repos (97.6%)
  - Low: 23455 repos (19.7%)
  - Informational: 51028 repos (42.8%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/pypa/sampleproject | 2770 |
| https://github.com/youtype/mypy_boto3_builder | 1329 |
| https://github.com/aliyun/alibabacloud-python-sdk | 478 |
| https://github.com/OCA/sale-workflow | 451 |
| https://github.com/pywinrt/pywinrt | 415 |
| https://github.com/Azure/azure-sdk-for-python | 407 |
| https://github.com/thejcannon/botocore-a-la-carte | 380 |
| https://github.com/aws/aws-cdk | 320 |
| https://github.com/OCA/purchase-workflow | 319 |
| https://github.com/OCA/stock-logistics-warehouse | 316 |
| https://github.com/liujianchao1214/PythonTest1 | 310 |
| https://github.com/OCA/stock-logistics-workflow | 280 |
| https://github.com/CoreOxide/aws_resource_validator | 278 |
| https://github.com/python/typeshed | 276 |
| https://github.com/TencentCloud/tencentcloud-sdk-python | 275 |
| https://github.com/MacHu-GWU/boto3_dataclass-project | 275 |
| https://github.com/airbytehq/airbyte | 272 |
| https://github.com/OCA/web | 270 |
| https://github.com/alipay/antchain-openapi-prod-sdk | 266 |
| https://github.com/OCA/account-invoicing | 260 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| unpinned-uses | High | 115592 | 97.0% | 1184419 |
| artipacked | Medium | 114247 | 95.9% | 398936 |
| excessive-permissions | Medium | 99885 | 83.9% | 387240 |
| secrets-outside-env | Medium | 64213 | 53.9% | 186703 |
| use-trusted-publishing | Informational | 43758 | 36.7% | 52774 |
| template-injection | Informational | 20626 | 17.3% | 135692 |
| cache-poisoning | High | 14280 | 12.0% | 28880 |
| superfluous-actions | Low | 11757 | 9.9% | 22151 |
| dangerous-triggers | High | 6812 | 5.7% | 9586 |
| archived-uses | Medium | 3688 | 3.1% | 7237 |
| secrets-inherit | Medium | 2547 | 2.1% | 12522 |
| unpinned-images | High | 1779 | 1.5% | 3652 |
| bot-conditions | High | 873 | 0.7% | 1061 |
| misfeature | Low | 510 | 0.4% | 1926 |
| unsound-condition | High | 414 | 0.3% | 576 |
| github-env | High | 375 | 0.3% | 912 |
| obfuscation | Low | 232 | 0.2% | 449 |
| overprovisioned-secrets | Medium | 201 | 0.2% | 340 |
| insecure-commands | High | 94 | 0.1% | 144 |
| unsound-contains | Informational | 83 | 0.1% | 187 |
| dependabot-cooldown | Medium | 23 | 0.0% | 28 |
| unredacted-secrets | Medium | 1 | 0.0% | 2 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| High | 116766 | 98.0% | 1294767 |
| Medium | 116296 | 97.6% | 916815 |
| Informational | 51028 | 42.8% | 116464 |
| Low | 23455 | 19.7% | 107371 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/langflow-ai/langflow | 12 | 771 | 2 |
| https://github.com/logspace-ai/langflow | 12 | 771 | 0 |
| https://github.com/khulnasoft/primeagent | 12 | 711 | 0 |
| https://github.com/aptos-labs/aptos-core | 12 | 670 | 7 |
| https://github.com/open-metadata/OpenMetadata | 12 | 467 | 3 |
| https://github.com/Significant-Gravitas/Auto-GPT | 12 | 275 | 3 |
| https://github.com/feldera/feldera | 12 | 241 | 0 |
| https://github.com/ansible/receptor | 12 | 121 | 1 |
| https://github.com/project-receptor/receptor | 12 | 121 | 0 |
| https://github.com/pytorch/pytorch | 11 | 1497 | 6944 |
| https://github.com/pkjmesra/pkscreener | 11 | 921 | 0 |
| https://github.com/Tencent/ncnn | 11 | 542 | 1 |
| https://github.com/aws/glide-for-redis | 11 | 433 | 0 |
| https://github.com/valkey-io/valkey-glide | 11 | 433 | 0 |
| https://github.com/servo/servo | 11 | 407 | 0 |
| https://github.com/passagemath/passagemath | 11 | 377 | 0 |
| https://github.com/man-group/arcticdb | 11 | 349 | 5 |
| https://github.com/hanzoai/studio-frontend | 11 | 342 | 0 |
| https://github.com/chroma-core/chroma | 11 | 322 | 344 |
| https://github.com/mcp-use/mcp-use | 11 | 265 | 0 |

## High severity (excluding unpinned-uses)

110425 findings across 33171 repos (27.8%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| cache-poisoning | 14280 | 28880 |
| template-injection | 12618 | 47213 |
| excessive-permissions | 8497 | 18237 |
| dangerous-triggers | 6812 | 9586 |
| unpinned-images | 1779 | 3652 |
| bot-conditions | 873 | 1061 |
| unsound-condition | 414 | 576 |
| github-env | 375 | 912 |
| insecure-commands | 94 | 144 |
| artipacked | 58 | 91 |
| unsound-contains | 42 | 73 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/passagemath/passagemath | 6 | 41 | 0 |
| https://github.com/invariant-systems-ai/aiir | 6 | 25 | 0 |
| https://github.com/Significant-Gravitas/Auto-GPT | 6 | 20 | 3 |
| https://github.com/microsoft/semantic-kernel | 6 | 13 | 10 |
| https://github.com/mapproxy/mapproxy | 6 | 12 | 0 |
| https://github.com/NVIDIA/cuda-quantum | 5 | 223 | 0 |
| https://github.com/nvidia/cuda-quantum | 5 | 223 | 0 |
| https://github.com/aptos-labs/aptos-core | 5 | 113 | 7 |
| https://github.com/khulnasoft/primeagent | 5 | 112 | 0 |
| https://github.com/langflow-ai/langflow | 5 | 111 | 2 |
| https://github.com/logspace-ai/langflow | 5 | 111 | 0 |
| https://github.com/pytorch/pytorch | 5 | 95 | 6944 |
| https://github.com/deckhouse/deckhouse | 5 | 89 | 0 |
| https://github.com/4paradigm/OpenMLDB | 5 | 84 | 0 |
| https://github.com/dimensionalOS/dimos-viewer | 5 | 83 | 0 |
| https://github.com/getretake/retake | 5 | 76 | 0 |
| https://github.com/OpenHands/software-agent-sdk | 5 | 72 | 0 |
| https://github.com/servo/servo | 5 | 69 | 0 |
| https://github.com/aws/glide-for-redis | 5 | 61 | 0 |
| https://github.com/valkey-io/valkey-glide | 5 | 61 | 0 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/deckhouse/deckhouse | 83277 | 9 | 8924 | 0 |
| https://github.com/swagger-api/swagger-codegen | 54105 | 8 | 6475 | 0 |
| https://github.com/cdklabs/cdk-cloudformation | 30199 | 5 | 2650 | 0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib | 28711 | 6 | 3243 | 172 |
| https://github.com/alibaba/loongsuite-python-agent | 28511 | 7 | 3217 | 0 |
| https://github.com/Azure/azureml-examples | 27103 | 5 | 2792 | 4 |
| https://github.com/tenstorrent/tt-metal | 19359 | 10 | 2519 | 0 |
| https://github.com/k2-fsa/sherpa-onnx | 16970 | 8 | 1801 | 0 |
| https://github.com/pytorch/pytorch | 13672 | 11 | 1497 | 6944 |
| https://github.com/open-telemetry/opentelemetry-python | 11007 | 5 | 1234 | 377 |
| https://github.com/sgl-project/sglang | 10251 | 10 | 1306 | 0 |
| https://github.com/topoteretes/cognee | 9980 | 10 | 1177 | 0 |
| https://github.com/airqo-platform/AirQo-api | 9830 | 6 | 1156 | 0 |
| https://github.com/microsoft/promptflow | 9049 | 8 | 902 | 10 |
| https://github.com/pkjmesra/pkscreener | 8166 | 11 | 921 | 0 |
| https://github.com/Goldziher/kreuzberg | 8159 | 6 | 850 | 0 |
| https://github.com/kreuzberg-dev/kreuzberg | 8119 | 7 | 845 | 0 |
| https://github.com/ClickHouse/ClickHouse | 7921 | 5 | 1895 | 0 |
| https://github.com/an0mium/aragora | 7918 | 9 | 1056 | 0 |
| https://github.com/NVIDIA/cuda-quantum | 7406 | 9 | 936 | 0 |
| https://github.com/nvidia/cuda-quantum | 7406 | 9 | 936 | 0 |
| https://github.com/opengamedata/opengamedata-core | 6735 | 7 | 723 | 0 |
| https://github.com/Z3Prover/z3 | 6708 | 9 | 731 | 64 |
| https://github.com/pulumi/pulumi-confluent | 6468 | 9 | 691 | 0 |
| https://github.com/langflow-ai/langflow | 6427 | 12 | 771 | 2 |
| https://github.com/logspace-ai/langflow | 6427 | 12 | 771 | 0 |
| https://github.com/dimensionalOS/dimos-viewer | 6408 | 10 | 702 | 0 |
| https://github.com/rhesis-ai/rhesis | 6241 | 6 | 899 | 0 |
| https://github.com/rerun-io/rerun | 6204 | 9 | 682 | 9 |
| https://github.com/predictable-labs/ryugraph | 6170 | 9 | 717 | 0 |
