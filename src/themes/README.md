# How the themes work

This guide is designed to help you understand how themes are structured in ManimStudio and how you can contribute your own themes to enhance the user experience. Whether you're looking to add a touch of personalization or contribute to the community, this guide will walk you through the process of creating and submitting new themes.

## Theme structure

In the current implementation every theme is contained in a module.

The module is a directory with the following structure:

```text
theme_name/
├── theme_name.json (usually this contains a lot of extra colors, but the app needs some of the colors, and that is why it is important to have a unified theme)
├── theme_name-variant1.json (this can be light, dark or any other variant)
├── theme_name-variant2.json...
```

Each module is then needs to be listed in the [themes.json](./themes.json) file with its variants.

## Example

As an example we can take the materialistic dark theme,from the [materialistic module](./materialistic/) module.

```json
{
  "name": "Materialistic Dark",
  "version": "1.0.0",
  "background": "#212121",
  "foreground": "#0d47a1",
  "primary": "#0288d1",
  "secondary": "#b3e5fc",
  "font": "#ffffff"
}
```

We can see that this contains most of the theme related information, however we need the [materialistic.json](./materialistic/materialistic.json)
for additional colors.

## Creating a new theme

Before you jump into creating a new theme, please check out the [contributing guidelines](../CONTRIBUTING.md).

After you created the new theme, please create a pull request with the new theme from your fork.

For any questions or assistance, feel free to reach out to us.

We encourage creativity and look forward to seeing your unique themes in ManimStudio!
