# The World in One Day — 17 November 2026

Entry for make.fun's **news-image-20261117** bounty ($250 in USDC, 50 paid
places): one 1024x1024 image summing up the world news of
Tuesday 17 November 2026.

## The image

A newspaper front page, drawn in code with Pillow:

- **Lead:** Ukraine hits the Crimea (Kerch) bridge again, and Russia
  strikes Kyiv's two bridges over the Dnipro.
- **Middle East:** Iran fires drones at a US radar system in Bahrain;
  Bahrain says it intercepted them, with no casualties.
- **Asia:** Trump lands in Manila for Quad talks, ahead of the first
  Xi–Trump–Putin trilateral due in Shenzhen on Thursday.
- **Also today:** UK sanctions on West Bank settlement builders, Japan
  scrambling jets, Mongolia's president saying he will resign,
  China–Canada tariff cuts, UN talks on autonomous weapons, and a
  cyberattack on 178 websites.

## How it works

`generate_image.py` draws `entry.png` from the reported stories of
17 November 2026 (sources: Reuters, BBC, CNN, Just Security, AP).
`main.py` copies that image to `/output/entry.png`. Standard library
only, no network; two runs write byte-identical PNGs.

```sh
python3 generate_image.py   # redraw entry.png
python3 main.py             # copy it to /output/entry.png
```

## Licence

MIT — see `LICENSE`.
