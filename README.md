A python script that validates menus from an API endpoint by 
checking whether the nodes in the menus contains 
cyclical references to themselves :smile:

### Usage

```python
    from validateMenus import *
    url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page="
    validateFromEndpoint(url) # accepts an URL and returns an JSON object 
```

The response from `validateFromEndpoint(url)` is an JSON object of the form 

```
{
  "valid_menus": [
    { "root_id": 2, "children": [1,3,4] },
  ],
  "invalid_menus": [
    { "root_id": 1, "children": [1,9,1] }
  ]
}
```

made with :heart: by Maxime 
