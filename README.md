# Transafe
## Online safe transactions made simple



[![Architecture-Services2.png](http://s16.postimg.org/i78r3rxed/Architecture_Services2.png)](http://postimg.org/image/6i4rft6fl/)


### How to run the Transafe Compositor

From Docker terminal:

```sh
$ cd ES-Compositor
$ docker build -t bernardomrf/compositor .
$ docker run -p 5001:5001 bernardomrf/compositor
```

Then just access the following URL:

  * 192.168.99.100:5001
