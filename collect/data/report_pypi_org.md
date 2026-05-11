# Zizmor scan report: pypi.org

- Packages fetched from pypi.org: 579673
  - No repo URL: 181439
  - github.com: 386958
  - gitlab.com: 7544
  - bitbucket.org: 3708
  - codeberg.org: 6
  - gitee.com: 2
  - generat0r.cc: 1
  - xxx.org: 1
  - gitlab.huajitech.net: 1
  - yahoo.com: 1
  - gitlab.axiros.com: 1
- Packages with GitHub repos: 386957 (343292 unique repos)
- Repos scanned: 122682
- Repos without workflows: 5889 (4.8%)
- Repos with findings: 120939 (98.6%)
- Total findings: 2290968
  - High: 119926 repos (97.8%)
  - Medium: 118050 repos (96.2%)
  - Low: 16194 repos (13.2%)
  - Informational: 56374 repos (46.0%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/pypa/sampleproject | 3067 |
| https://github.com/youtype/mypy_boto3_builder | 1332 |
| https://github.com/aliyun/alibabacloud-python-sdk | 480 |
| https://github.com/OCA/sale-workflow | 460 |
| https://github.com/CoreOxide/aws_resource_validator | 443 |
| https://github.com/pywinrt/pywinrt | 415 |
| https://github.com/Azure/azure-sdk-for-python | 409 |
| https://github.com/thejcannon/botocore-a-la-carte | 380 |
| https://github.com/liujianchao1214/PythonTest1 | 326 |
| https://github.com/OCA/purchase-workflow | 325 |
| https://github.com/OCA/stock-logistics-warehouse | 321 |
| https://github.com/aws/aws-cdk | 320 |
| https://github.com/OCA/stock-logistics-workflow | 283 |
| https://github.com/python/typeshed | 276 |
| https://github.com/MacHu-GWU/boto3_dataclass-project | 275 |
| https://github.com/TencentCloud/tencentcloud-sdk-python | 275 |
| https://github.com/OCA/web | 273 |
| https://github.com/airbytehq/airbyte | 272 |
| https://github.com/alipay/antchain-openapi-prod-sdk | 270 |
| https://github.com/OCA/account-invoicing | 262 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| unpinned-uses | High | 118485 | 96.6% | 1213167 |
| artipacked | Medium | 117468 | 95.7% | 413473 |
| excessive-permissions | Medium | 102235 | 83.3% | 393682 |
| use-trusted-publishing | Informational | 44181 | 36.0% | 53294 |
| template-injection | Informational | 21166 | 17.3% | 134441 |
| cache-poisoning | High | 15371 | 12.5% | 30871 |
| superfluous-actions | Informational | 11286 | 9.2% | 13587 |
| dangerous-triggers | High | 7025 | 5.7% | 9847 |
| archived-uses | Medium | 3625 | 3.0% | 7027 |
| secrets-inherit | Medium | 2593 | 2.1% | 12295 |
| unpinned-images | High | 1784 | 1.5% | 3694 |
| bot-conditions | High | 911 | 0.7% | 1135 |
| misfeature | Low | 519 | 0.4% | 1864 |
| unsound-condition | High | 405 | 0.3% | 570 |
| github-env | High | 379 | 0.3% | 883 |
| obfuscation | Low | 234 | 0.2% | 438 |
| overprovisioned-secrets | Medium | 205 | 0.2% | 340 |
| insecure-commands | High | 92 | 0.1% | 140 |
| unsound-contains | Informational | 83 | 0.1% | 189 |
| dependabot-cooldown | Medium | 24 | 0.0% | 29 |
| unredacted-secrets | Medium | 1 | 0.0% | 2 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| High | 119926 | 97.8% | 1329227 |
| Medium | 118050 | 96.2% | 741032 |
| Informational | 56374 | 46.0% | 127080 |
| Low | 16194 | 13.2% | 93629 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/langflow-ai/langflow | 11 | 743 | 2 |
| https://github.com/logspace-ai/langflow | 11 | 743 | 0 |
| https://github.com/khulnasoft/primeagent | 11 | 631 | 0 |
| https://github.com/pkjmesra/pkscreener | 11 | 407 | 0 |
| https://github.com/Significant-Gravitas/Auto-GPT | 11 | 237 | 3 |
| https://github.com/feldera/feldera | 11 | 237 | 0 |
| https://github.com/ansible/receptor | 11 | 110 | 1 |
| https://github.com/project-receptor/receptor | 11 | 110 | 0 |
| https://github.com/pytorch/pytorch | 10 | 781 | 6944 |
| https://github.com/Tencent/ncnn | 10 | 529 | 1 |
| https://github.com/passagemath/passagemath | 10 | 360 | 0 |
| https://github.com/hanzoai/studio-frontend | 10 | 305 | 0 |
| https://github.com/chroma-core/chroma | 10 | 292 | 344 |
| https://github.com/Keeper-Security/secrets-manager | 10 | 279 | 3 |
| https://github.com/mcp-use/mcp-use | 10 | 248 | 0 |
| https://github.com/pietrozullo/mcpeer | 10 | 248 | 0 |
| https://github.com/amd/gaia | 10 | 224 | 0 |
| https://github.com/pulumi/pulumi | 10 | 222 | 116 |
| https://github.com/checkmarx/kics | 10 | 188 | 0 |
| https://github.com/flipt-io/flipt-client-sdks | 10 | 170 | 0 |

## High severity (excluding unpinned-uses)

116137 findings across 34918 repos (28.5%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| cache-poisoning | 15371 | 30871 |
| template-injection | 13110 | 49074 |
| excessive-permissions | 9190 | 19760 |
| dangerous-triggers | 7025 | 9847 |
| unpinned-images | 1784 | 3694 |
| bot-conditions | 911 | 1135 |
| unsound-condition | 405 | 570 |
| github-env | 379 | 883 |
| insecure-commands | 92 | 140 |
| artipacked | 56 | 89 |
| unsound-contains | 43 | 74 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/passagemath/passagemath | 6 | 41 | 0 |
| https://github.com/invariant-systems-ai/aiir | 6 | 27 | 0 |
| https://github.com/feldera/feldera | 6 | 19 | 0 |
| https://github.com/Significant-Gravitas/Auto-GPT | 6 | 18 | 3 |
| https://github.com/microsoft/semantic-kernel | 6 | 13 | 10 |
| https://github.com/mapproxy/mapproxy | 6 | 12 | 0 |
| https://github.com/NVIDIA/cuda-quantum | 5 | 229 | 0 |
| https://github.com/nvidia/cuda-quantum | 5 | 229 | 0 |
| https://github.com/langflow-ai/langflow | 5 | 116 | 2 |
| https://github.com/logspace-ai/langflow | 5 | 116 | 0 |
| https://github.com/khulnasoft/primeagent | 5 | 112 | 0 |
| https://github.com/pytorch/pytorch | 5 | 107 | 6944 |
| https://github.com/getretake/retake | 5 | 89 | 0 |
| https://github.com/4paradigm/OpenMLDB | 5 | 84 | 0 |
| https://github.com/an0mium/aragora | 5 | 83 | 0 |
| https://github.com/OpenHands/software-agent-sdk | 5 | 80 | 0 |
| https://github.com/vllm-project/vllm-ascend | 5 | 71 | 0 |
| https://github.com/aws/glide-for-redis | 5 | 69 | 0 |
| https://github.com/valkey-io/valkey-glide | 5 | 69 | 0 |
| https://github.com/servo/servo | 5 | 66 | 0 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/swagger-api/swagger-codegen | 53745 | 8 | 6436 | 0 |
| https://github.com/cdklabs/cdk-cloudformation | 30135 | 4 | 2642 | 0 |
| https://github.com/alibaba/loongsuite-python-agent | 28799 | 6 | 3249 | 0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib | 25923 | 5 | 2936 | 172 |
| https://github.com/tenstorrent/tt-metal | 17751 | 9 | 2332 | 0 |
| https://github.com/Azure/azureml-examples | 17581 | 4 | 1734 | 4 |
| https://github.com/k2-fsa/sherpa-onnx | 14561 | 8 | 1631 | 0 |
| https://github.com/sgl-project/sglang | 11621 | 9 | 1464 | 0 |
| https://github.com/open-telemetry/opentelemetry-python | 10029 | 5 | 1125 | 377 |
| https://github.com/microsoft/promptflow | 8905 | 7 | 886 | 10 |
| https://github.com/ayutaz/piper-plus | 8430 | 9 | 930 | 0 |
| https://github.com/ClickHouse/ClickHouse | 8128 | 4 | 1959 | 0 |
| https://github.com/an0mium/aragora | 7506 | 9 | 987 | 0 |
| https://github.com/airqo-platform/AirQo-api | 7356 | 5 | 881 | 0 |
| https://github.com/NVIDIA/cuda-quantum | 7303 | 7 | 922 | 0 |
| https://github.com/nvidia/cuda-quantum | 7303 | 7 | 922 | 0 |
| https://github.com/kreuzberg-dev/kreuzberg | 7190 | 5 | 696 | 0 |
| https://github.com/pytorch/pytorch | 7109 | 10 | 781 | 6944 |
| https://github.com/Goldziher/kreuzberg | 6404 | 5 | 628 | 0 |
| https://github.com/langflow-ai/langflow | 6221 | 11 | 743 | 2 |
| https://github.com/logspace-ai/langflow | 6221 | 11 | 743 | 0 |
| https://github.com/pulumi/pulumi-confluent | 6174 | 7 | 658 | 0 |
| https://github.com/rhesis-ai/rhesis | 6110 | 5 | 880 | 0 |
| https://github.com/ai16z/eliza | 6071 | 9 | 801 | 0 |
| https://github.com/elizaos/eliza | 6071 | 9 | 801 | 0 |
| https://github.com/coqui-ai/STT | 5853 | 7 | 663 | 0 |
| https://github.com/slint-ui/slint | 5808 | 6 | 638 | 0 |
| https://github.com/pulumi/pulumi-yandex | 5644 | 7 | 597 | 0 |
| https://github.com/rerun-io/rerun | 5499 | 8 | 602 | 9 |
| https://github.com/Tencent/BqLog | 5375 | 7 | 558 | 0 |
