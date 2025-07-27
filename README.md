# aerocosmos

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Server setup

Windows:
```sh
cd ./backend

pip install -r ./requirements.txt
```

Unix:
```sh
cd ./backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Compile and Hot-Reload for Development

Windows:
```sh
npm run dev:win
```

Unix:
```sh
npm run dev
```

## Run app demo

```sh
npm run electron:start
```

## Build
after Project setup!

### Linux

prepare wheelhouse:
```sh
python3 -m pip install -U pip wheel

python3 -m pip wheel -r backend/requirements.txt -w wheelhouse
```

prepare standalone python:

#### For Linux:
```sh
source ./scripts/pbs.lock

curl -L -o pbs.tar.gz "https://github.com/astral-sh/python-build-standalone/releases/download/${PBS_RELEASE}/cpython-${PYTHON}+${PBS_RELEASE}-${LINUX_TARGET}-install_only.tar.gz"

tar --use-compress-program=unzstd -xf pbs.tar.gz

mkdir -p build/python-linux && rsync -a python/ build/python-linux/
```

#### For Windows:
```sh
source ./scripts/pbs.lock

curl -L -o pbs.tar.gz "https://github.com/astral-sh/python-build-standalone/releases/download/${PBS_RELEASE}/cpython-${PYTHON}+${PBS_RELEASE}-${WIN_TARGET}-install_only.tar.gz"

tar --use-compress-program=unzstd -xf pbs.tar.gz

mkdir -p build/python-win && rsync -a python/ build/python-win/
```