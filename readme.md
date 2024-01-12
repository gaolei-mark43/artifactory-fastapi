# Artifactory存储库管理工具

该项目是一个使用 FastAPI 框架的 Python Web 应用程序，主要用于管理和查询 Artifactory 存储库的信息。以下是一些主要功能的简要概述：

## 获取存储总表

通过 `/storageinfo` 端点，可以获取所有存储库的信息。

## 获取单表存储

通过 `/storageinfo/{repo_name}` 端点，可以获取指定存储库的信息。

## 获取虚拟库、远程库和本地库

通过 `/virtual_repo`，`/remote_repo` 和 `/local_repo` 端点，可以获取虚拟库、远程库和本地库的信息。

## 获取单库数据

通过 `/repo/{repo_name}` 端点，可以获取指定库的数据。

## 获取制品锁定用户

通过 `/depnd_lock_user`，`/pub_artifacts_lock_user` 和 `/artifacts_lock_user` 端点，可以获取私服锁定用户、公网制品锁定用户和办公网制品锁定用户的信息。

## 解锁ARF用户

通过 `/unlock_all_user` 端点，可以解锁所有 ARF 用户。

## 查询单库下载数据

通过 `/table/{repo_name}` 端点，可以查询指定库的下载数据。

## 获取各种类型库的下载数据

通过 `/mvn_remote`，`/mvn_local`，`/npm`，`/pypi`，`/cocoapods`，`/conan`，`/conda`，`/pub` 和
`/mvn_temp` 端点，可以获取 maven-remote，maven-local，npm，pypi，cocoapods，conan，conda，pub 和 mvn_temp 类型的库的下载数据。

 `restart.sh` 脚本，用于重启应用程序。该脚本首先会杀死当前正在运行的进程，然后启动一个新的进程。

这个工具可以帮助开发者和管理员更好地管理和理解他们的 Artifactory 存储库。