# Prior Authorization Rule Design — Requirements, Test Cases & Defect Log

A simulation of the business-analyst lifecycle for a new Medicaid pharmacy prior authorization rule, from requirements through testing and defect documentation.

## Scenario

GLP-1 medications prescribed for chronic weight management represent a fast-growing, high-cost category of Medicaid pharmacy spend. This project defines a dedicated prior authorization rule for this drug category, then tests whether a (simulated) claims system correctly implements it.

## Contents

- **[BRD_PA_GLP1_WeightManagement](output/BRD_PA_GLP1_WeightManagement.pdf)** — Business Requirements Document defining the business need, objective, scope, and explicit approval/denial/pend criteria for the new rule.
- **[PA_GLP1_Test_Case_Matrix.xlsx](output/PA_GLP1_Test_Case_Matrix.xlsx)** — two sheets:
  - **Test Case Matrix**: 25 synthetic test scenarios covering positive cases, negative cases, boundary/edge cases, and missing-data cases. Each row's "System Expected Outcome" is a live Excel formula implementing the BRD's logic, compared against an "Actual System Outcome" with a PASS/FAIL result.
  - **Defect Log**: 3 defects that testing surfaced, each with severity, root-cause hypothesis, and a recommended resolution.

## Business Rule Summary

A claim is **Approved** only if all of the following are true: approved obesity diagnosis code, documented BMI ≥ 30, age ≥ 18, step therapy on file, and quantity ≤ 1 fill per 28-day supply. Missing required data routes to **Pend**; present-but-failing data routes to **Deny**.

## Defects Found

| ID | Issue | Severity |
|---|---|---|
| DEF-001 | Quantity exceeding the limit was approved instead of denied | High |
| DEF-002 | Missing BMI was denied instead of pended | Medium |
| DEF-003 | Diabetes-indication diagnosis was approved under the weight-management rule instead of denied as out of scope | High |

## Note

This is a synthetic exercise built for demonstration — no real patient data, PA system, or claims processor is involved. It is intended to show a defensible approach to requirements documentation and test design for a pharmacy benefit business rule.
