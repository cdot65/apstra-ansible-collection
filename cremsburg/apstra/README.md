# Ansible Collection - cremsburg.apstra

[![N|Solid](https://gitlab.com/_calvinr/networking/apstra-ansible-collection/-/raw/master/static/img/apstra.png)](https://juniper.net/)

## `Overview`

The goal of this collection is to provide an easier way to interact with Juniper's Apstra solution. While nothing will stop you from using the built-in module, you may find that working with pre-packaged modules can help simplify the development of your playbook, or it may just be easier to support as a team.

## 📋 `Apstra version compatibility`

For Apstra 3.x and lower, please continue to use the collection at version 0.0.17; there are some significant changes with Apstra 4.x releases and this collection will try to focus on the latest releases.

## 📋 `Ansible version compatibility`

Ansible is going through some rapid changes and while those changes get worked out we will continue to test for Ansible 2.10.x.

It is unlikely that something will break on later Ansible versions, but something to keep in mind.

## ⚙️ `Batteries Included`

Here is a short list of modules included within the collection, expect feature parity with the Swagger before this project hits `version 0.1.0`

Name | Description
---- | -----------
[cremsburg.apstra.blueprint](https://gitlab.com/_calvinr/networking/apstra-ansible-collection/-/blob/master/cremsburg/apstra/docs/cremsburg.apstra.blueprint.rst)|Manage Blueprints
[cremsburg.apstra.design](https://gitlab.com/_calvinr/networking/apstra-ansible-collection/-/blob/master/cremsburg/apstra/docs/cremsburg.apstra.design.rst)|Manage the Design elements
[cremsburg.apstra.resources](https://gitlab.com/_calvinr/networking/apstra-ansible-collection/-/blob/master/cremsburg/apstra/docs/cremsburg.apstra.resources.rst)|Manage the Resources elements

## 🚀 `Executing the playbook`

After installing the collections, you can call the modules by using their full name path.

`test.yaml`

```yaml
---
- hosts: localhost
  gather_facts: False
  become: False
  tasks:
    
    - name: "### CREATE IP POOL cicd_leaf_loopbacks"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        display_name: "cicd_leaf_loopbacks"
        type: "ip-pools"
        tags:
          - cicd
          - leaf
        subnets:
          - "10.255.2.0/24"

        # define to delete or create
        state: present
```

Then simply run your playbook

```sh
ansible-playbook test.yaml
```

If you used Ansible Vault to encrypt your secrets, you need to append the `--ask-vault-pass` to your command.

## ⚠️ Very Important! ⚠️

Please make sure to manage your sensative information carfully. While the modules support the parameter of `api_key`, this should never be statically entered with your token in clear text.

Here are better alternatives:

### Manage your API token as an environmental

```sh
export APSTRA_API_TOKEN='YOUR_PRIVATE_KEY_HERE'
```

> you can also use `APSTRA_API_KEY`, if you prefer

### Manage your API token as a secret with Ansible Vault

create a file to store your API token in

`$ vim vault.yaml`

```yaml
api_token: "MY_APSTRA_API_TOKEN_HERE"
```

encrypt the new file

```sh
ansible-vault encrypt vault.yml
```

and now you'll need to pass your vault password when using the playbook

```sh
ansible-playbook --ask-vault-pass test.yaml
```

## Development

Want to contribute? Great!

Submit a PR and let's work on this together :D
