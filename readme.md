# Blender Rez Package

[Rez](https://github.com/AcademySoftwareFoundation/rez) package definition for [Blender](https://www.blender.org)'s official releases.

## Building and Releasing

The script downloads the official Blender release for the target version, platform and architecture, and packages it as a Rez package.

Linux:

```sh
rez build --variants 0
# or
rez release --variants 0
```

Windows:

```sh
rez build --variants 1
# or
rez release --variants 1
```