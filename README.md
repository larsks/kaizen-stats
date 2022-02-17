This is a hacky little collection of scripts that pull some summary data from an OpenStack deployment.

To run the scripts:

```
python generate_stats.py
```

This will produce `stats.json` with content along the lines of:

```
{
  "53b3586a-af33-4c50-93b4-081206d674a1": {
    "name": "My Awesome Project",
    "server_count": 10,
    "flavor_ram": 303104,
    "flavor_vcpus": 116,
    "volume_count": 18,
    "volume_size": 1280
  },
  [...]
}
```
