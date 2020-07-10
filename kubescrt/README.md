# kubescrt
### While getting sensative data from Kubernetes is simple, it could be simpler!

`kubescrt` is a simple tool to quickly read secrets in Kubernetes.

#### Get Secret keys
```bash
kubescrt [SECRET NAME]
```

#### Get Secret keys and values
```bash
kubescrt -s [SECRET NAME]
```

#### Dependencies
- JQ