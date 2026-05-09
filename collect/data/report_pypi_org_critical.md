# Zizmor scan report: pypi.org

- Packages fetched from pypi.org: 523
  - No repo URL: 23
  - github.com: 499
  - gitlab.com: 1
- Packages with GitHub repos: 499 (459 unique repos)
- Repos scanned: 415
- Repos without workflows: 45 (10.8%)
- Repos with findings: 378 (91.1%)
- Total findings: 15069
  - High: 354 repos (85.3%)
  - Medium: 367 repos (88.4%)
  - Low: 158 repos (38.1%)
  - Informational: 105 repos (25.3%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/googleapis/google-cloud-python | 13 |
| https://github.com/Azure/azure-sdk-for-python | 12 |
| https://github.com/open-telemetry/opentelemetry-python | 8 |
| https://github.com/grpc/grpc | 4 |
| https://github.com/python/typeshed | 3 |
| https://github.com/tensorflow/tensorboard | 2 |
| https://github.com/psycopg/psycopg2 | 2 |
| https://github.com/jupyter-widgets/ipywidgets | 2 |
| https://github.com/apache/airflow | 2 |
| https://github.com/Legrandin/pycryptodome | 2 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| artipacked | Medium | 352 | 84.8% | 2755 |
| unpinned-uses | High | 330 | 79.5% | 7446 |
| excessive-permissions | Medium | 293 | 70.6% | 2186 |
| secrets-outside-env | Medium | 170 | 41.0% | 894 |
| template-injection | Informational | 104 | 25.1% | 708 |
| cache-poisoning | High | 69 | 16.6% | 183 |
| superfluous-actions | Low | 59 | 14.2% | 88 |
| dangerous-triggers | High | 57 | 13.7% | 118 |
| use-trusted-publishing | Informational | 46 | 11.1% | 95 |
| unpinned-images | High | 20 | 4.8% | 113 |
| bot-conditions | High | 13 | 3.1% | 15 |
| archived-uses | Medium | 10 | 2.4% | 32 |
| secrets-inherit | Medium | 10 | 2.4% | 290 |
| obfuscation | Low | 9 | 2.2% | 16 |
| misfeature | Low | 8 | 1.9% | 104 |
| unsound-condition | High | 3 | 0.7% | 5 |
| github-env | High | 2 | 0.5% | 4 |
| insecure-commands | High | 2 | 0.5% | 13 |
| unsound-contains | Informational | 2 | 0.5% | 3 |
| overprovisioned-secrets | Medium | 1 | 0.2% | 1 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| Medium | 367 | 88.4% | 5271 |
| High | 354 | 85.3% | 8218 |
| Low | 158 | 38.1% | 1180 |
| Informational | 105 | 25.3% | 400 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/pytorch/pytorch | 11 | 1497 | 6944 |
| https://github.com/aio-libs/yarl | 10 | 81 | 846 |
| https://github.com/aio-libs/multidict | 10 | 66 | 550 |
| https://github.com/huggingface/transformers | 9 | 515 | 2589 |
| https://github.com/apache/arrow | 9 | 333 | 2480 |
| https://github.com/SeleniumHQ/selenium | 9 | 153 | 1518 |
| https://github.com/pypa/hatch | 9 | 142 | 98 |
| https://github.com/google/flatbuffers | 9 | 137 | 204 |
| https://github.com/huggingface/tokenizers | 9 | 92 | 380 |
| https://github.com/aio-libs/aiohttp | 9 | 77 | 5267 |
| https://github.com/aio-libs/frozenlist | 9 | 56 | 442 |
| https://github.com/googleapis/google-cloud-python | 8 | 338 | 476 |
| https://github.com/googleapis/python-storage | 8 | 338 | 652 |
| https://github.com/apache/spark | 8 | 240 | 588 |
| https://github.com/snowflakedb/snowflake-connector-python | 8 | 140 | 185 |
| https://github.com/huggingface/huggingface_hub | 8 | 108 | 665 |
| https://github.com/getsentry/sentry-python | 8 | 65 | 504 |
| https://github.com/shapely/shapely | 8 | 54 | 1400 |
| https://github.com/huggingface/safetensors | 8 | 53 | 247 |
| https://github.com/aio-libs/async-lru | 8 | 39 | 108 |

## High severity (excluding unpinned-uses)

772 findings across 144 repos (34.7%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| cache-poisoning | 69 | 183 |
| dangerous-triggers | 57 | 118 |
| template-injection | 55 | 223 |
| unpinned-images | 20 | 113 |
| excessive-permissions | 17 | 98 |
| bot-conditions | 13 | 15 |
| unsound-condition | 3 | 5 |
| insecure-commands | 2 | 13 |
| github-env | 2 | 4 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/pytorch/pytorch | 5 | 95 | 6944 |
| https://github.com/getsentry/sentry-python | 5 | 21 | 504 |
| https://github.com/apache/arrow | 4 | 38 | 2480 |
| https://github.com/pypa/hatch | 4 | 11 | 98 |
| https://github.com/jupyterlab/jupyterlab | 4 | 9 | 970 |
| https://github.com/scikit-learn/scikit-learn | 4 | 9 | 8580 |
| https://github.com/huggingface/huggingface_hub | 4 | 7 | 665 |
| https://github.com/snowflakedb/snowflake-connector-python | 4 | 6 | 185 |
| https://github.com/huggingface/transformers | 3 | 48 | 2589 |
| https://github.com/aws/sagemaker-python-sdk | 3 | 30 | 66 |
| https://github.com/apache/spark | 3 | 27 | 588 |
| https://github.com/great-expectations/great_expectations | 3 | 19 | 58 |
| https://github.com/Azure/azure-sdk-for-python | 3 | 12 | 408 |
| https://github.com/SeleniumHQ/selenium | 3 | 9 | 1518 |
| https://github.com/aio-libs/aiohttp | 3 | 8 | 5267 |
| https://github.com/dulwich/dulwich | 3 | 8 | 148 |
| https://github.com/pyca/bcrypt | 3 | 6 | 494 |
| https://github.com/snowflakedb/snowflake-sqlalchemy | 3 | 6 | 109 |
| https://github.com/databricks/databricks-sdk-py | 3 | 5 | 49 |
| https://github.com/python/typeshed | 3 | 5 | 1100 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/pytorch/pytorch | 13672 | 11 | 1497 | 6944 |
| https://github.com/open-telemetry/opentelemetry-python | 11007 | 5 | 1234 | 377 |
| https://github.com/huggingface/transformers | 4093 | 9 | 515 | 2589 |
| https://github.com/apache/arrow | 2853 | 9 | 333 | 2480 |
| https://github.com/googleapis/google-cloud-python | 2838 | 8 | 338 | 476 |
| https://github.com/googleapis/python-storage | 2838 | 8 | 338 | 652 |
| https://github.com/great-expectations/great_expectations | 2455 | 7 | 278 | 58 |
| https://github.com/apache/spark | 2093 | 8 | 240 | 588 |
| https://github.com/langchain-ai/langchain | 1933 | 7 | 226 | 165 |
| https://github.com/dmlc/xgboost | 1695 | 7 | 209 | 684 |
| https://github.com/SeleniumHQ/selenium | 1463 | 9 | 153 | 1518 |
| https://github.com/fastapi/fastapi | 1402 | 7 | 153 | 2920 |
| https://github.com/snowflakedb/snowflake-connector-python | 1268 | 8 | 140 | 185 |
| https://github.com/pypa/hatch | 1260 | 9 | 142 | 98 |
| https://github.com/jupyterlab/jupyterlab | 1240 | 6 | 154 | 970 |
| https://github.com/google/flatbuffers | 1176 | 9 | 137 | 204 |
| https://github.com/scikit-learn/scikit-learn | 1072 | 7 | 118 | 8580 |
| https://github.com/pylint-dev/pylint | 1018 | 5 | 100 | 3360 |
| https://github.com/jupyter-server/jupyter_server | 948 | 4 | 111 | 276 |
| https://github.com/jupyter/jupyter_core | 856 | 4 | 97 | 242 |
| https://github.com/snowflakedb/snowflake-sqlalchemy | 852 | 7 | 88 | 109 |
| https://github.com/aws/sagemaker-python-sdk | 846 | 7 | 85 | 66 |
| https://github.com/fastapi/typer | 836 | 6 | 93 | 2391 |
| https://github.com/jupyter/jupyter_client | 811 | 4 | 93 | 426 |
| https://github.com/opencv/opencv-python | 807 | 6 | 115 | 3545 |
| https://github.com/ipython/ipykernel | 801 | 5 | 94 | 1558 |
| https://github.com/sphinx-doc/sphinx | 800 | 4 | 68 | 7351 |
| https://github.com/jupyter/notebook | 789 | 6 | 83 | 705 |
| https://github.com/ipython/traitlets | 763 | 4 | 87 | 484 |
| https://github.com/opensearch-project/opensearch-py | 757 | 7 | 87 | 110 |
