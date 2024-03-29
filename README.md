# `prefect` code examples

<details>
<summary>Contributing</summary>

## steps for contributing an example
- clone this repo
- `pip install httpx pre-commit pydantic`
- `pre-commit install`
- create a new file in the `examples` directory under an appropriate subdirectory
- include helpful comments in your example
- open a PR!

</details>

## examples
### `flows`: using the `@flow` decorator
- [basic flow usage](examples/flows/basic.py)
- [basic async flow usage](examples/flows/async_basic.py)

### `tasks`: using the `@task` decorator
- [basic task usage](examples/tasks/basic.py)
- [submitting task runs](examples/tasks/submitting.py)

### `deployments`: remote configuration and execution of flows
- [(serve) a basic ETL that processes inputs](examples/deployments/serve.py)