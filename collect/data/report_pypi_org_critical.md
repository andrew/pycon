# Zizmor scan report: pypi.org

- Packages fetched from pypi.org: 523
  - No repo URL: 23
  - github.com: 499
  - gitlab.com: 1
- Packages with GitHub repos: 499 (459 unique repos)
- Repos scanned: 409
- Repos without workflows: 45 (11.0%)
- Repos with findings: 352 (86.1%)
- Total findings: 12157
  - High: 333 repos (81.4%)
  - Medium: 325 repos (79.5%)
  - Low: 118 repos (28.9%)
  - Informational: 129 repos (31.5%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/googleapis/google-cloud-python | 13 |
| https://github.com/Azure/azure-sdk-for-python | 12 |
| https://github.com/open-telemetry/opentelemetry-python | 8 |
| https://github.com/grpc/grpc | 4 |
| https://github.com/python/typeshed | 3 |
| https://github.com/Legrandin/pycryptodome | 2 |
| https://github.com/apache/airflow | 2 |
| https://github.com/jupyter-widgets/ipywidgets | 2 |
| https://github.com/psycopg/psycopg2 | 2 |
| https://github.com/tensorflow/tensorboard | 2 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| artipacked | Medium | 334 | 81.7% | 2329 |
| unpinned-uses | High | 305 | 74.6% | 6326 |
| excessive-permissions | Medium | 278 | 68.0% | 1873 |
| template-injection | Informational | 97 | 23.7% | 708 |
| cache-poisoning | High | 63 | 15.4% | 172 |
| dangerous-triggers | High | 56 | 13.7% | 105 |
| superfluous-actions | Informational | 48 | 11.7% | 58 |
| use-trusted-publishing | Informational | 44 | 10.8% | 93 |
| unpinned-images | High | 17 | 4.2% | 70 |
| bot-conditions | High | 11 | 2.7% | 11 |
| archived-uses | Medium | 10 | 2.4% | 15 |
| secrets-inherit | Medium | 9 | 2.2% | 282 |
| misfeature | Low | 7 | 1.7% | 75 |
| obfuscation | Low | 7 | 1.7% | 14 |
| unsound-condition | High | 3 | 0.7% | 5 |
| github-env | High | 2 | 0.5% | 4 |
| insecure-commands | High | 2 | 0.5% | 13 |
| unsound-contains | Informational | 2 | 0.5% | 3 |
| overprovisioned-secrets | Medium | 1 | 0.2% | 1 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| High | 333 | 81.4% | 7037 |
| Medium | 325 | 79.5% | 3731 |
| Informational | 129 | 31.5% | 491 |
| Low | 118 | 28.9% | 898 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/pytorch/pytorch | 10 | 781 | 6944 |
| https://github.com/huggingface/tokenizers | 9 | 78 | 380 |
| https://github.com/aio-libs/yarl | 9 | 77 | 846 |
| https://github.com/aio-libs/multidict | 9 | 64 | 550 |
| https://github.com/huggingface/transformers | 8 | 447 | 2589 |
| https://github.com/pypa/hatch | 8 | 132 | 98 |
| https://github.com/SeleniumHQ/selenium | 8 | 129 | 1518 |
| https://github.com/google/flatbuffers | 8 | 124 | 204 |
| https://github.com/aio-libs/aiohttp | 8 | 77 | 5267 |
| https://github.com/aio-libs/frozenlist | 8 | 54 | 442 |
| https://github.com/apache/spark | 7 | 235 | 588 |
| https://github.com/huggingface/huggingface_hub | 7 | 130 | 665 |
| https://github.com/snowflakedb/snowflake-connector-python | 7 | 109 | 185 |
| https://github.com/shapely/shapely | 7 | 52 | 1400 |
| https://github.com/aio-libs/async-lru | 7 | 38 | 108 |
| https://github.com/aio-libs/aiosignal | 7 | 26 | 419 |
| https://github.com/dmlc/xgboost | 6 | 199 | 684 |
| https://github.com/great-expectations/great_expectations | 6 | 170 | 58 |
| https://github.com/jupyterlab/jupyterlab | 6 | 161 | 970 |
| https://github.com/scikit-learn/scikit-learn | 6 | 117 | 8580 |

## High severity (excluding unpinned-uses)

711 findings across 135 repos (33.0%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| cache-poisoning | 63 | 172 |
| dangerous-triggers | 56 | 105 |
| template-injection | 53 | 227 |
| excessive-permissions | 18 | 104 |
| unpinned-images | 17 | 70 |
| bot-conditions | 11 | 11 |
| unsound-condition | 3 | 5 |
| insecure-commands | 2 | 13 |
| github-env | 2 | 4 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/pytorch/pytorch | 5 | 107 | 6944 |
| https://github.com/getsentry/sentry-python | 4 | 20 | 504 |
| https://github.com/huggingface/tokenizers | 4 | 20 | 380 |
| https://github.com/Azure/azure-sdk-for-python | 4 | 18 | 408 |
| https://github.com/pypa/hatch | 4 | 12 | 98 |
| https://github.com/jupyterlab/jupyterlab | 4 | 10 | 970 |
| https://github.com/scikit-learn/scikit-learn | 4 | 10 | 8580 |
| https://github.com/snowflakedb/snowflake-connector-python | 4 | 6 | 185 |
| https://github.com/huggingface/transformers | 3 | 49 | 2589 |
| https://github.com/aws/sagemaker-python-sdk | 3 | 30 | 66 |
| https://github.com/apache/spark | 3 | 27 | 588 |
| https://github.com/great-expectations/great_expectations | 3 | 20 | 58 |
| https://github.com/SeleniumHQ/selenium | 3 | 9 | 1518 |
| https://github.com/aio-libs/aiohttp | 3 | 8 | 5267 |
| https://github.com/dulwich/dulwich | 3 | 8 | 148 |
| https://github.com/pyca/bcrypt | 3 | 6 | 494 |
| https://github.com/python/typeshed | 3 | 5 | 1100 |
| https://github.com/aio-libs/async-lru | 3 | 4 | 108 |
| https://github.com/aio-libs/async-timeout | 3 | 4 | 824 |
| https://github.com/aio-libs/multidict | 3 | 4 | 550 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/open-telemetry/opentelemetry-python | 10029 | 5 | 1125 | 377 |
| https://github.com/pytorch/pytorch | 7109 | 10 | 781 | 6944 |
| https://github.com/huggingface/transformers | 3556 | 8 | 447 | 2589 |
| https://github.com/apache/spark | 2062 | 7 | 235 | 588 |
| https://github.com/apache/arrow | 1960 | 4 | 189 | 2480 |
| https://github.com/dmlc/xgboost | 1599 | 6 | 199 | 684 |
| https://github.com/great-expectations/great_expectations | 1479 | 6 | 170 | 58 |
| https://github.com/jupyterlab/jupyterlab | 1315 | 6 | 161 | 970 |
| https://github.com/SeleniumHQ/selenium | 1253 | 8 | 129 | 1518 |
| https://github.com/pypa/hatch | 1170 | 8 | 132 | 98 |
| https://github.com/scikit-learn/scikit-learn | 1064 | 6 | 117 | 8580 |
| https://github.com/google/flatbuffers | 1047 | 8 | 124 | 204 |
| https://github.com/pylint-dev/pylint | 1009 | 4 | 99 | 3360 |
| https://github.com/snowflakedb/snowflake-connector-python | 989 | 7 | 109 | 185 |
| https://github.com/jupyter-server/jupyter_server | 898 | 4 | 105 | 276 |
| https://github.com/jupyter/jupyter_core | 856 | 4 | 97 | 242 |
| https://github.com/jupyter/jupyter_client | 811 | 4 | 93 | 426 |
| https://github.com/opencv/opencv-python | 807 | 6 | 115 | 3545 |
| https://github.com/ipython/ipykernel | 792 | 4 | 93 | 1558 |
| https://github.com/sphinx-doc/sphinx | 782 | 3 | 66 | 7351 |
| https://github.com/jupyter/notebook | 780 | 5 | 82 | 705 |
| https://github.com/ipython/traitlets | 763 | 4 | 87 | 484 |
| https://github.com/aio-libs/aiohttp | 733 | 8 | 77 | 5267 |
| https://github.com/python/typeshed | 726 | 5 | 75 | 1100 |
| https://github.com/opensearch-project/opensearch-py | 691 | 6 | 80 | 110 |
| https://github.com/aws/sagemaker-python-sdk | 684 | 6 | 67 | 66 |
| https://github.com/networkx/networkx | 678 | 5 | 83 | 3160 |
| https://github.com/aio-libs/yarl | 677 | 9 | 77 | 846 |
| https://github.com/jupyterlab/jupyterlab_server | 648 | 5 | 74 | 67 |
| https://github.com/snowflakedb/snowflake-sqlalchemy | 605 | 5 | 61 | 109 |
