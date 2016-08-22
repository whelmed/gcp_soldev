package greeter

import (
  "fmt"
  "net/http"
  "appengine"
  "appengine/datastore"
)

type Greeting struct {
    Message string
}

func init() {
  http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
  c := appengine.NewContext(r)
  q := datastore.NewQuery("Greeting")

  var greetings []Greeting
  keys, err := q.GetAll(c, &greetings)

  if err != nil {
      fmt.Fprint(w, err)
      return
  }

  for i, _ := range greetings {
          k := keys[i]

          var g Greeting
          datastore.Get(c, k, &g)
          fmt.Fprint(w, g.Message)

          g.Message += " from Go!"
          datastore.Put(c, k, &g)

  }

}
