# How To: Embed Splunk Dashboard in Unbranded Webpage using iFrame

## Splunk-side

To hide options in the timeframe/timerange dropdowns, add the following code *within* the fieldset tags associated with the dropdown:

```html
    <html>
      <style>
        div[id^='advanced_view'] {
          display: none;
        }
      </style>
    </html>
```