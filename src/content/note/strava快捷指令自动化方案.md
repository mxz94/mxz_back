---
pubDatetime: 2024-06-25 14:10:40
title: strava快捷指令自动化方案
slug: strava快捷指令自动化方案
tags:
- "工具"
---

最近下班骑车20km，每次都要打开strava软件点击记录，再打开音乐， 现在想有一个自动化的方案。  
1. iphone 的快捷指令设置  url Schemes  打开url 会自动记录  
2. iphone 设置自动化， 离开某地时自动打开  
  
URL Schemes: URL 方案：  
strava:// *works for all URL schemes  
strava:// *适用于所有 URL 方案  
  
stravaride:// *works for some URL schemes  
stravaride:// *适用于某些 URL 方案  
  
stravarun:// *works for some URL schemes  
stravarun:// *适用于某些 URL 方案  
  
record/ *opens record page  
记录/ *打开记录页面  
  
record/settings *opens the settings in the record page  
记录/设置 *在记录页面中打开设置  
  
record/new/start *starts a new recording  
record/new/start *开始新录制  
  
record/new/pause *pauses current recording  
record/new/pause *暂停当前录制  
  
record/new/resume *resumes current recording  
录制/新建/恢复 *恢复当前录制  
  
record/new/settings *opens the settings in the record page  
record/new/settings *在记录页面中打开设置  
  
activities/ 活动/  
  
activities/new *creates a manual activity  
activities/new *创建手动活动  
  
activities/{id}  活动/{id}  
  
activities/{id}/kudos  活动/{id}/kudos  
  
activities/{id}/comments  
活动/{id}/comments  
  
activities/{id}/analysis  
活动/{id}/分析  
  
activities/{id}/results  活动/{id}/结果  
  
athletes/ 运动员/  
  
athletes/search  运动员/搜索  
  
athletes/{id}  运动员/{id}  
  
athletes/{id}/activities  
运动员/{id}/活动  
  
athletes/{id}/routes  运动员/{id}/routes  
  
athletes/{id}/segments  运动员/{id}/段  
  
athletes/{id}/following  运动员/{id}/关注  
  
athletes/{id}/followers  运动员/{id}/追随者  
  
athletes/{id}/challenges  
运动员/{id}/挑战  
  
athletes/{id}/clubs  运动员/{id}/俱乐部  
  
athletes/{id}/trophy-case  
运动员/{id}/奖杯箱  
  
athletes/{id}/gear  运动员/{id}/装备  
  
clubs/  梅花/  
  
clubs/search  俱乐部/搜索  
  
clubs/{id} *using "clubs/{id}/", instead of "clubs/{id}" will log you out  
clubs/{id} *使用“clubs/{id}/”，而不是“clubs/{id}”将注销  
  
clubs/{id}/invite  俱乐部/{id}/邀请  
  
clubs/{id}/stats  俱乐部/{id}/stats  
  
clubs/{id}/members  俱乐部/{id}/会员  
  
clubs/{id}/settings  clubs/{id}/设置  
  
challenges/  挑战/  
  
challenges/{id}  挑战/{id}  
  
premium/ *opens subscription page  
高级版/ *打开订阅页面  
  
athlete/ *opens logged in athlete's page  
运动员/ *打开已登录的运动员页面  
  
athlete/activities  运动员/活动  
  
athlete/activities/search  
运动员/活动/搜索  
  
athlete/profile *opens profile section for athlete  
运动员/个人资料 *打开运动员个人资料部分  
  
athlete/segments  运动员/分段  
  
athlete/following  运动员/追随者  
  
athlete/followers  运动员/追随者  
  
athlete/progress *opens progress section for athlete  
运动员/进度 *打开运动员的进度部分  
  
athlete/training  运动员/训练  
  
routes/  路线/  
  
routes/search  路线/搜索  
  
routes/new  路线/新  
  
routes/{id}  路由/{id}  
  
segments/  段/  
  
segments/{id}  段/{id}  
  
settings/  设置/  
  
settings/profile  设置/配置文件  
  
settings/change-password  
设置/更改密码  
  
settings/change-email  设置/更改电子邮件  
  
settings/privacy  设置/隐私  
  
settings/privacy/profile-page  
设置/隐私/个人资料页面  
  
settings/privacy/activities  
设置/隐私/活动  
  
settings/privacy/mentions  
设置/隐私/提及  
  
settings/privacy/blocked-accounts  
设置/隐私/阻止帐户  
  
settings/push-notifications  
设置/推送通知