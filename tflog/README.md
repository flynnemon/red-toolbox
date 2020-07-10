# tflog
### Adding persistant logging and rollbacks to Terraform since 2020!

`tflog` is a simple wrapper for `Terraform` that captures all stdout in console and in a persistant log file. In addition, `tflog` creates a backup of the current state automaticaly before important `Terraform` commands.

```bash
tflog [standard terraform arguments]
```

#### Dependencies
- Terraform