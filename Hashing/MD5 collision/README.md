MD5 was depracticed in 2004 because it can cause has collisions, check the example below:

```
md5sum plane.jpg | awk '{print $1}' >> plane_sum
md5sum ship.jpg | awk '{print $1}' >> ship_sum
diff plane_sum ship_sum
```

![Pic 1: ](./plane.jpg)
![Pic 2:](./ship.jpg)

Both images have the same MD5 hash while being completely different images (253dd04e87492e4fc3471de5e776bc3d)
