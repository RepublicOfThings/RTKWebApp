# How To: Embed Splunk Dashboard in Unbranded Webpage using iFrame

## Splunk-side

Make sure the permissions are set correctly for a dashboard (i.e. dashboard is readable by user).

In a dashboard, go to 'Edit', select 'Source' tab.
 
For each panel in the dashboard source, add the following tag:

```html
    <option name="link.visible">false</option>
```

This will disable inspection & search links in the panel, preventing users from transitioning to SplunkWeb directly.

In the ````html <form>```` tag, add the following arguments:

```html
    <form hideSplunkBar="true" hideFooter="true" hideEdit="true" hideChrome="true" hideAppBar="true">
```

These arguments will hide Splunk branding (footer, header, navigation), and disable editing features for the page.

Next up, the web.conf file needs to be modified to allow access to iframes. This can be done by setting:

```
x_frame_options_sameorigin = 0
enable_insecure_login = 1
```

This also enables insecure login features. Note that it may be possible that the User's password is *publicly visible*
which may present a security issue in some contexts.

#### Note

If hideEdit is true, the option will disappear from the rendered dashboard to edit it (duh!). However, to carry out 
further edits, append 'edit' to the URL, as below:

```html
http://<host>:<port>/en-US/app/<app-name>/<dashboard>/edit
```


## Django-side

Embedding an iframe is trivial. Simply add the following line of code to any html page:
```html
<iframe src="http://<target>/en-US/account/insecurelogin?username=<usr>&password=<pwd>&return_to=app/search/<target>"></iframe>
```

Note that formatting and style should be added to this -- it'll look very ugly as-is!