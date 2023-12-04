# Adding a new widget to the DebiAI dashboard

After [starting the DebiAI in development mode](https://debiai.irt-systemx.fr/introduction/gettingStarted/installation/development.html), you can create a folder in the `frontend/src/components/debiai/dataAnalysis/widgets` directory with the name of your widget for example: `MyWidget`.

## Configuration

Create a `configuration.json` file in the directory :

```json
// In widgets/MyWidget/configuration.json
{
  "name": "Widget name",
  "description": "Widget description",

  // Optional fields:
  "layout": {
    // Size of the widget when played in the dashboard
    "width": 5,
    "minWidth": 2,
    "maxWidth": 15,
    "height": 4,
    "minHeight": 2,
    "maxHeight": 15
  },

  // Categories and project types are used to filter the widgets in the dashboard
  "categories": ["Model evaluation"],
  "projectTypes": ["Classification"],

  // Link to the widget documentation, the link will be added automatically in the widget catalogue
  "documentationLink": "https://debiai.irt-systemx.fr/dashboard/widgets/confusion_matrix/"
}
```

## Icon

Add a squared `icon.png` file in the directory, it will be displayed in the widget catalogue.

## Widget code

Finally create a `MyWidget.vue` file in the directory.
This is the main file of your widget, **it must have the same name as the folder**.

Refer to the `WidgetTemplateEmpty` and `WidgetTemplateFull` template widgets available in the widgets directory to have something to start with.

If you need help with the code, feel free to start a discussion in on [GitHub](https://github.com/debiai/debiai/discussions/categories/widget-creation)

Here is the complete widget API documentation, is shows how to make your widget interact with the dashboard:
![Widget AP](DebiAI-widget-api.png)
