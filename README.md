# Open Telemetry Dashboard

This is a simple dashboard for viewing robot (or I guess anything) telemetry data. If you can get it into a python dictionary as a list of numbers it will display a trendline updating at whatever frequency you ask for. 

I need to emphasize that this is not a production ready dashboard and was built to serve the needs of making a functional dashboard for combat robotics. It is full of hacks and bad practices. This was 30 minutes of fiddling to get it working followed by a few hours of trying to make it usable for people other than me. 

## Installation
`pip install -r requirements.txt` 
`npm install`

## Running
`npm run start-dev` will start a development server on port 5001. This will handle live reloading of the templates and will recompile the css on change.

`npm run start` will start a 'production' server on port 5000.

## Deployment

Seriously, if you deploy this somewhere you should probably use something else. 

## Adding Custom Data
Ok, this is just html/css and server sent events. You wanna add new data? Just write some html and ship it from the server. If you can read it from a python script  and stuff it into the dictionary it'll work. In `app.py` there's a `fetch_data` function that currently just adds a random value to the previous value. You can update this. It's run in a separate thread than the webserver but make sure to sleep for a bit in it. Please note, all fields are currently sent to all connections so only add data that you actually need to display. 

To add it to the frontend you can make rows of charts:
```
<div hx-ext="sse" sse-connect="/telemetry?hz=1" class="flex flex-row gap-4 flex-wrap mt-8 mx-auto container text-center">
    <div class="text-3xl my-auto">(&nbsp;1 hz)</div> 
    {{ sparkline.sparkline("voltage") }}
</div>
```

where the string passed to sparkline is the name of the data you want to display. It will be updated at the frequency you specify in the telemetry endpoint (default is 30hz. You can add mutliple sparklines to the same parent div and they will only open a single connection to the server. If you really don't like how this causes layouts you could use something like css grid to re-arrange the elements while still maintaining the dom structure to share an SSE connection

If you have styling requiements - it's just tailwind, either you are probably familiar with it or ChatGPT can help you out.

## How
This project uses (abuses) htmx and htmx server sent events to provide a live updating dashboard. The sparklines are a webfont. It's hacky but it works. 