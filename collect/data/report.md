# Zizmor scan report

- Packages fetched from PyPI: 533073
  - No repo URL: 159358
  - github.com: 362899
  - gitlab.com: 7299
  - bitbucket.org: 3510
  - codeberg.org: 4
  - generat0r.cc: 1
  - xxx.org: 1
  - GitHub.com: 1
- Packages with GitHub repos: 362899 (323202 unique repos)
- Repos scanned: 17325
- Repos without workflows: 5889 (34.0%)
- Repos with findings: 17026 (98.3%)
- Total findings: 512464
  - High: 16694 repos (96.4%)
  - Medium: 16713 repos (96.5%)
  - Low: 5264 repos (30.4%)
  - Informational: 6751 repos (39.0%)

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
| unpinned-uses | High | 16364 | 94.5% | 240337 |
| artipacked | Medium | 16268 | 93.9% | 80842 |
| excessive-permissions | Medium | 15119 | 87.3% | 81311 |
| secrets-outside-env | Medium | 9437 | 54.5% | 46396 |
| use-trusted-publishing | Informational | 5326 | 30.7% | 6903 |
| template-injection | Informational | 3723 | 21.5% | 34765 |
| cache-poisoning | High | 2434 | 14.0% | 5886 |
| superfluous-actions | Low | 1872 | 10.8% | 3766 |
| dangerous-triggers | High | 1726 | 10.0% | 2706 |
| secrets-inherit | Medium | 746 | 4.3% | 5198 |
| archived-uses | Medium | 559 | 3.2% | 1208 |
| unpinned-images | High | 458 | 2.6% | 1147 |
| bot-conditions | High | 209 | 1.2% | 264 |
| misfeature | Low | 172 | 1.0% | 854 |
| github-env | High | 106 | 0.6% | 281 |
| overprovisioned-secrets | Medium | 93 | 0.5% | 146 |
| unsound-condition | High | 88 | 0.5% | 145 |
| obfuscation | Low | 75 | 0.4% | 173 |
| unsound-contains | Informational | 38 | 0.2% | 85 |
| insecure-commands | High | 28 | 0.2% | 47 |
| dependabot-cooldown | Medium | 3 | 0.0% | 4 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| Medium | 16713 | 96.5% | 192057 |
| High | 16694 | 96.4% | 266414 |
| Informational | 6751 | 39.0% | 21004 |
| Low | 5264 | 30.4% | 32989 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/langflow-ai/langflow | 12 | 771 | 2 |
| https://github.com/aptos-labs/aptos-core | 12 | 670 | 7 |
| https://github.com/open-metadata/OpenMetadata | 12 | 467 | 3 |
| https://github.com/Significant-Gravitas/Auto-GPT | 12 | 275 | 3 |
| https://github.com/feldera/feldera | 12 | 241 | 0 |
| https://github.com/ansible/receptor | 12 | 121 | 1 |
| https://github.com/pytorch/pytorch | 11 | 1497 | 6944 |
| https://github.com/pkjmesra/pkscreener | 11 | 921 | 0 |
| https://github.com/Tencent/ncnn | 11 | 542 | 1 |
| https://github.com/valkey-io/valkey-glide | 11 | 433 | 0 |
| https://github.com/passagemath/passagemath | 11 | 377 | 0 |
| https://github.com/man-group/arcticdb | 11 | 349 | 5 |
| https://github.com/chroma-core/chroma | 11 | 322 | 344 |
| https://github.com/mcp-use/mcp-use | 11 | 265 | 0 |
| https://github.com/elementary-data/elementary | 11 | 203 | 0 |
| https://github.com/flipt-io/flipt-client-sdks | 11 | 184 | 0 |
| https://github.com/pulumi/pulumi | 11 | 177 | 116 |
| https://github.com/microsoft/semantic-kernel | 11 | 167 | 10 |
| https://github.com/pulumi/pulumi-eks | 11 | 152 | 1 |
| https://github.com/pulumi/pulumi-kubernetes | 11 | 142 | 5 |

## High severity (excluding unpinned-uses)

26104 findings across 5717 repos (33.0%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| template-injection | 2440 | 12759 |
| cache-poisoning | 2434 | 5886 |
| dangerous-triggers | 1726 | 2706 |
| excessive-permissions | 1076 | 2831 |
| unpinned-images | 458 | 1147 |
| bot-conditions | 209 | 264 |
| github-env | 106 | 281 |
| unsound-condition | 88 | 145 |
| insecure-commands | 28 | 47 |
| unsound-contains | 16 | 18 |
| artipacked | 9 | 20 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/passagemath/passagemath | 6 | 41 | 0 |
| https://github.com/Significant-Gravitas/Auto-GPT | 6 | 20 | 3 |
| https://github.com/microsoft/semantic-kernel | 6 | 13 | 10 |
| https://github.com/mapproxy/mapproxy | 6 | 12 | 0 |
| https://github.com/NVIDIA/cuda-quantum | 5 | 223 | 0 |
| https://github.com/aptos-labs/aptos-core | 5 | 113 | 7 |
| https://github.com/langflow-ai/langflow | 5 | 111 | 2 |
| https://github.com/pytorch/pytorch | 5 | 95 | 6944 |
| https://github.com/deckhouse/deckhouse | 5 | 89 | 0 |
| https://github.com/OpenHands/software-agent-sdk | 5 | 72 | 0 |
| https://github.com/valkey-io/valkey-glide | 5 | 61 | 0 |
| https://github.com/llamastack/llama-stack | 5 | 47 | 0 |
| https://github.com/ansible/awx | 5 | 45 | 2 |
| https://github.com/treeverse/lakeFS | 5 | 39 | 4 |
| https://github.com/kreuzberg-dev/tree-sitter-language-pack | 5 | 38 | 0 |
| https://github.com/dbt-labs/dbt-core | 5 | 33 | 139 |
| https://github.com/PennyLaneAI/pennylane | 5 | 30 | 49 |
| https://github.com/PostHog/posthog | 5 | 30 | 0 |
| https://github.com/astronomer/astro-sdk | 5 | 28 | 2 |
| https://github.com/Chia-Network/chia-blockchain | 5 | 27 | 3 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/deckhouse/deckhouse | 83277 | 9 | 8924 | 0 |
| https://github.com/cdklabs/cdk-cloudformation | 30199 | 5 | 2650 | 0 |
| https://github.com/open-telemetry/opentelemetry-python-contrib | 28711 | 6 | 3243 | 172 |
| https://github.com/Azure/azureml-examples | 27103 | 5 | 2792 | 4 |
| https://github.com/k2-fsa/sherpa-onnx | 16970 | 8 | 1801 | 0 |
| https://github.com/pytorch/pytorch | 13672 | 11 | 1497 | 6944 |
| https://github.com/open-telemetry/opentelemetry-python | 11007 | 5 | 1234 | 377 |
| https://github.com/sgl-project/sglang | 10251 | 10 | 1306 | 0 |
| https://github.com/topoteretes/cognee | 9980 | 10 | 1177 | 0 |
| https://github.com/microsoft/promptflow | 9049 | 8 | 902 | 10 |
| https://github.com/pkjmesra/pkscreener | 8166 | 11 | 921 | 0 |
| https://github.com/kreuzberg-dev/kreuzberg | 8119 | 7 | 845 | 0 |
| https://github.com/NVIDIA/cuda-quantum | 7406 | 9 | 936 | 0 |
| https://github.com/Z3Prover/z3 | 6708 | 9 | 731 | 64 |
| https://github.com/langflow-ai/langflow | 6427 | 12 | 771 | 2 |
| https://github.com/rerun-io/rerun | 6204 | 9 | 682 | 9 |
| https://github.com/aptos-labs/aptos-core | 6071 | 12 | 670 | 7 |
| https://github.com/HumanSignal/label-studio | 5809 | 10 | 666 | 1 |
| https://github.com/roboflow/inference | 5767 | 9 | 604 | 3 |
| https://github.com/Opentrons/opentrons | 5370 | 9 | 669 | 3 |
| https://github.com/kreuzberg-dev/tree-sitter-language-pack | 5367 | 8 | 551 | 0 |
| https://github.com/kuzudb/kuzu | 5265 | 9 | 617 | 3 |
| https://github.com/OpenAPITools/openapi-generator | 5228 | 10 | 594 | 0 |
| https://github.com/quic/ai-hub-models | 5227 | 8 | 612 | 0 |
| https://github.com/PennyLaneAI/pennylane-lightning | 5225 | 9 | 631 | 6 |
| https://github.com/redhat-performance/benchmark-runner | 5084 | 7 | 591 | 0 |
| https://github.com/osohq/oso | 4985 | 9 | 549 | 4 |
| https://github.com/pantsbuild/pants | 4966 | 8 | 522 | 8 |
| https://github.com/DataDog/integrations-core | 4870 | 9 | 686 | 0 |
| https://github.com/ERGO-Code/HiGHS | 4717 | 7 | 726 | 13 |
