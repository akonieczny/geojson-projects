# GeoJSON projects

## Developer setup
1. Clone repo:
    ```shell
    git clone git@github.com:akonieczny/geojson-projects.git
    ```
2. Go to project directory
    ```shell
    cd geojson-projects
    ```
3. Setup project manually
    1. Create and activate virtual environment
        ```shell
        python3.12 -m venv .venv
        source ./.venv/bin/activate
        ```
    2. Install pip-tools
        ```shell
        pip install pip-tools
        ```
    3. Install python requirements
        ```shell
        bash ./scripts/sync_pip.sh
        ```
4. Or setup project with script
    ```shell
    bash ./scripts/setup_project.sh
    ```

## Run project
### Using venv
```shell
bash ./infrastructure/start.local.sh
```
### Using docker-compose
```shell
docker-compose up -d
```
