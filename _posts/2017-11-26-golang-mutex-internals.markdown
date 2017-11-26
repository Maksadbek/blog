---
layout: post
title:  "Golang mutex internals"
date:   2017-11-26 20:46:40 +0500
categories: golang
---
## Intro

## The difference between Mutex and RWmutex in Golang

### Intro
Usually we use mutual expressions in Go to protect memory area from mutation by multiple goroutines in the same time.
Golang include two types of mutexes in `sync` package: `sync.Mutex` and `sync.RWmutex`
The difference is explained below

### Mutex use cases
Lets take an example of simple struct that include a `map` that keeps count of visitor by country.
```Golang
m := map[sting]int
```
And we have multiple HTTP handlers that increments this counters.

```
func Increment(r http.Request, w *http.ResponseWriter) {
  r.FormParse()
  country := r.Form.Get("country")
  m[country]++
}
```
As each handlers runs on separate goroutine, all of them try to increment the map at the same time.
In this case to protect the memory from this, we must use mutexes, this requires to create a struct and keep map within it:
We are embedding `sync.Mutex` in our struct.
```
type Counter struct {
  Visitors map[string]int
  sync.Mutex
}
```
And slightly change our handler and Counter struct:
We firstly create a instance
```
  // Add increment methods
  func (c Counter) Inc(countryName string) {
     // lock the `c`, other goroutines are not able to mutate it while it is locked,
     // they have to wait until it is unlocked
    c.Lock()
    c.Visitors[countryName]++
    c.Unlock()
  }
  c := Counter{}
```
We use `Inc` method in handlers
```
func Increment(r http.Request, w *http.ResponseWriter) {
  r.FormParse()
  country := r.Form.Get("country")
  c.Inc(country)
}
```

**Note**
If you're keeping a struct in the map:
```
type County struct {
  Visitors int 
}
m := map[string]Country{}
```

And try to increment a `Visitors` directly from the map:
```
m["Uzbekistan"].Visitors++
```

This will run into the following error:
```
cannot assign to m["Uzbekistan"].Visitors
```
Because accessing directly to struct fields in the map is not allowed.

### Use of `RWmutex`
