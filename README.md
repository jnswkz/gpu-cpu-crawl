## Small crawler for GPU and CPU specs from [TechPowerUp](https://www.techpowerup.com/) 

## How to use
1. Install pixi from [here](https://pixi.sh/latest/)

2. Install dependencies
```bash
pixi install
```

3. Run the script
- CPU crawler
```bash
pixi run cpucrawl
```
- GPU crawler
```bash
pixi run gpucrawl
```

> Note: If receive too many 429 status code, try to refresh the [site](https://www.techpowerup.com/cpu-specs) or add more delay to `time.sleep()` function in the script. (CPU crawler)

> Feel free to use my json files
