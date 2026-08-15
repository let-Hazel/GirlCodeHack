# README — Community Safety Assistance Platform

## Problem Statement

Underserved communities often face delayed responses to local safety incidents due to limited resources and poor communication channels. Residents may not have a reliable way to quickly inform nearby community members who could assist with non-severe incidents, while serious incidents may need to be escalated to the appropriate authorities.

## Proposed Solution

The proposed system is a **community safety reporting and assistance platform** that connects residents with people nearby who may be able to assist with local incidents.

When a resident reports an incident, nearby community members can view the report and indicate whether they are able to help. This allows communities to respond to incidents that can safely be handled locally.

For incidents that are **severe or require professional intervention**, the system can escalate the report to the appropriate authorities.

The system therefore follows a simple principle:

```text
Incident reported
       ↓
Nearby community members notified
       ↓
Can the community assist?
   ↙             ↘
 Yes              No / Severe
  ↓                  ↓
Community        Escalate to
assistance       authorities
```

## Main Features

### 1. Report an Incident

A resident can report a local safety incident by providing information such as:

* Incident type.
* Location.
* Description.
* Severity.
* Time of incident.
* Optional supporting information.

### 2. Notify Nearby Community Members

Once an incident is reported, relevant nearby community members can be notified.

They can view information about the incident and decide whether they are able and willing to assist.

### 3. Community Assistance

For incidents that do not require emergency services, community members can offer assistance.

For example:

* Helping someone who needs immediate but non-emergency assistance.
* Checking on a nearby community member.
* Providing relevant information.
* Helping direct people away from an unsafe area.
* Connecting the person with an appropriate local resource.

### 4. Severity Assessment

Reports can be categorised according to their severity.

For example:

```text
LOW
↓
Community assistance may be sufficient

MEDIUM
↓
Community assistance + monitoring

HIGH / SEVERE
↓
Escalate to appropriate authorities
```

### 5. Authority Escalation

If an incident is severe, dangerous, or requires professional intervention, the system should provide an escalation pathway to the appropriate authorities.

The community should **not be expected to handle dangerous situations themselves**.

### 6. Incident Status

Users can see the progress of an incident:

```text
Reported
   ↓
Community Notified
   ↓
Assistance Offered
   ↓
Being Handled
   ↓
Resolved
```

For severe incidents:

```text
Reported
   ↓
Identified as Severe
   ↓
Escalated
   ↓
Authority Response
   ↓
Resolved
```

## Example Scenario

A resident notices that an elderly neighbour needs assistance.

They submit a report through the platform.

Nearby community members receive the notification. One person who is close by and able to help responds to the report.

The incident is therefore handled within the community without unnecessarily involving emergency services.

However, if a resident reports a serious crime, fire, or another situation requiring professional emergency intervention, the report is escalated to the relevant authorities instead of asking community members to put themselves in danger.

## Goals

The system aims to:

1. Improve communication between nearby community members.
2. Encourage safe community-based assistance.
3. Reduce unnecessary delays in getting help.
4. Identify incidents that require professional intervention.
5. Provide an escalation pathway for severe incidents.
6. Create a central record of reported community safety incidents.

## Target Users

* Community residents.
* Community volunteers.
* Community safety representatives.
* Relevant authorities or emergency responders.

## Core Principle

The platform is **not intended to replace emergency services**.

Instead, it creates a communication layer between community members:

> **If the community can safely help, enable the community to help. If the situation is severe, escalate it to the appropriate authorities.**

## Expected Impact

The platform aims to strengthen communication within underserved communities by allowing nearby residents to become aware of incidents that they may be able to safely assist with, while ensuring that serious incidents can be escalated to people with the appropriate resources and authority.
