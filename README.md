# fomo-telegram-bot

This is a simple telegram bot to forward messages from many telegram chat to one designated chat or channel.
Forwarding is made by putting hashtag "#fomo" in message or in reply to forwarded message.

## Configuration

This bot is configured by `config.yaml`.

Config example:
```yaml
bot:
  token: "{bot token}"
  forward_channel_id: "{designated chat id to forward messages}"
  allowed_source_ids:
    - "{chat ids}"
  admin_users:
    - "{list of admin usernames}"

```

- `bot.token` - bot token. Alternate source of token - `FOMO_BOT_TOKEN` env variable (has priority to `congig.yaml`).
- `bot.forward_channel_id` - String id. Designated chat id to forward messages.
- `bot.allowed_source_ids` - List of string ids. Only messages from those chats will be forwarded.
- `bot.admin_users` - List of string usernames. List of admin users.

## Commands

### /admin

`/admin` - Show chat id.

Only users listed as admins in config can call this command.

## Build

This project uses [dogebuild](https://github.com/dogebuild/dogebuild) in [make mode](https://dogebuild.readthedocs.io/en/latest/make-mode/) to provide simple and cross platform way to build project.

`config.yaml` is necessary to build docker container.

## Deploy

### Ansible

I recommend to use [Ansible](https://www.ansible.com/) for deploying this bot.

Here is ansible playbook example
```yaml
- hosts: bot-host
  gather_facts: True
  vars_prompt:
  - name: token
    prompt: Enter bot token

  tasks:
  - name: Install aptitude
    apt:
      name: aptitude
      state: latest
      update_cache: true

  - name: Install required system packages
    apt:
      pkg:
        - apt-transport-https
        - ca-certificates
        - curl
        - software-properties-common
        - python3-pip
        - virtualenv
        - python3-setuptools
      state: latest
      update_cache: true

  - name: Add Docker GPG apt Key
    apt_key:
      url: https://download.docker.com/linux/ubuntu/gpg
      state: present

  - name: Add Docker Repository
    apt_repository:
      repo: deb https://download.docker.com/linux/ubuntu focal stable
      state: present

  - name: Update apt and install docker-ce
    apt:
      name: docker-ce
      state: latest
      update_cache: true

  - name: Start docker
    systemd:
      name: docker
      state: started
      enabled: yes
      daemon_reload: yes

  - name: Install python libraries to support ansible work with docker
    pip:
      name:
      - docker
      - docker-compose

  - name: Install dogebuild
    pip:
      name: dogebuild
    delegate_to: localhost

  - name: Checkout git
    git:
      repo: git@github.com:kirillsulim/fomo-telegram-bot.git
      dest: ./git
      single_branch: yes
      version: prod
      depth: 1
    delegate_to: localhost

  - name: Copy config
    copy:
      src: config.yaml
      dest: ./git/config.yaml
    delegate_to: localhost

  - name: Build container
    command: "doge -f ./git/dogefile.py build_tar"
    delegate_to: localhost

  - name: Create a directory for fomo-bot
    file:
      path: /srv/fomo-bot
      state: directory

  - name: Upload container to server
    copy:
      src: ./git/build/fomo-bot.tar
      dest: /srv/fomo-bot/fomo-bot.tar

  - name: Load image
    command: "docker load --input /srv/fomo-bot/fomo-bot.tar"

  - name: Start docker container
    docker_container:
      image: fomo-bot
      name: fomo-bot
      restart_policy: on-failure
      env:
        FOMO_BOT_TOKEN: "{{ token }}"
```

For this example to work you must put `config.yaml` in playbook directory.
Please note that in this playbook bot token is provided at playbook run to avoid storing secret data in playbook repository.


## Chat bootstrap

0. Deploy your bot.
1. Add bot to channel disignated to forward messages as administrator.
2. Write test message. It seems that you cannot get username or user id in channel so you have to extract channel id
   from  logs.
3. Add channel id to configuration.
4. Add bot to all groups you want to forward messages from.
5. Post "/admin" command to all groups.
6. Add chat ids to configuration.
7. Redeploy your bot with new configuration.