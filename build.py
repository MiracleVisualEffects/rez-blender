import os
import urllib.request
import shutil
import subprocess

extMap = {"linux": "tar.xz", "windows": "zip", "mac": "dmg"}
downloadUrlTemplate = "https://download.blender.org/release/Blender{vmaj}.{vmin}/blender-{vstr}-{platform}-{arch}.{ext}"


def copytree(src, dst):
    # Check if rclone is available
    rclone_path = shutil.which("rclone")
    if rclone_path:
        print("Using rclone to copy files...")
        subprocess.run(
            [
                rclone_path,
                "copy",
                src,
                dst,
                "--transfers",
                "64",
                "--checkers",
                "64",
                "--copy-links",
                "--create-empty-src-dirs",
            ],
            check=True,
        )
    else:
        print("rclone not found, using shutil.copytree...")
        shutil.copytree(src, dst, dirs_exist_ok=True)


def build():
    requires = os.environ["REZ_BUILD_VARIANT_REQUIRES"].split()
    platform = requires[0].split("-")[1]
    arch = requires[1].split("-")[1].replace("x86_64", "x64")
    vstr = os.environ["REZ_BUILD_PROJECT_VERSION"]
    v = vstr.split(".")

    downloadUrl = downloadUrlTemplate.format(
        vmaj=v[0],
        vmin=v[1],
        vstr=vstr,
        platform=platform,
        arch=arch,
        ext=extMap[platform],
    )

    srcPath = os.environ["REZ_BUILD_SOURCE_PATH"]
    buildPath = os.environ["REZ_BUILD_PATH"]
    installPath = os.environ["REZ_BUILD_INSTALL_PATH"]
    doInstall = os.environ["REZ_BUILD_INSTALL"] == "1"

    archiveName = downloadUrl.split("/")[-1]
    archivePath = os.path.join(srcPath, archiveName)

    expectedExtractPath = os.path.join(
        srcPath,
        f"blender-{vstr}-{platform}-{arch}",
    )

    if os.path.exists(archivePath):
        print(f"Skipping download, archive already exists at {archivePath}.")
    else:
        print(f"Downloading Blender from {downloadUrl}...")
        urllib.request.urlretrieve(downloadUrl, archivePath)
        print("Download complete.")

    if not os.path.exists(archivePath):
        raise RuntimeError(f"Archive not found at: {archivePath}")

    if os.path.exists(expectedExtractPath):
        print(f"Skipping extraction, folder already exists at {expectedExtractPath}.")
    else:
        print(f"Extracting Blender archive {archivePath}...")
        shutil.unpack_archive(archivePath, srcPath)
        print("Extraction complete.")

    if not os.path.exists(expectedExtractPath):
        raise RuntimeError(
            f"Expected extracted path does not exist: {expectedExtractPath}"
        )

    if doInstall:
        print(f"Installing Blender to {installPath}...")
        copytree(expectedExtractPath, installPath)

        if platform != "windows":
            print("Setting executable permissions for Blender binaries...")
            binaries = ["blender", "blender-launcher", "blender-softwaregl"]
            for binary in binaries:
                os.chmod(
                    os.path.join(installPath, binary),
                    0o755,
                )
            print("Permissions set.")

        print("Installation complete.")
    else:
        print("Skipping installation step.")


if __name__ == "__main__":
    build()
