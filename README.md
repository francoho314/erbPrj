# $${\color{red}Bookstore Management System (Website)} $$
# $${\color{red}書店管理系統 (網店版) }$$
$${\color{green}      By Python, Django, PostgreSQL}$$
### Certificate in Python Web Framework Development Assistant  
### Python 網站框架開發助理證書  
##### The Course of Employees Retraining Baord (ERB), HKSAR, China  
##### 香港特別行政區ERB僱員再培訓局課程  

-----
**Course Code:** &nbsp;&nbsp;&nbsp;CT290DS007  
**Team Name:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AFFA  
**Team Member:** &nbsp;Alice Hui, Franco Ho, Felix Ng,Antoninus Yeung  
**Date Create:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;29 August 2025  
**Project Aims:** &nbsp;&nbsp;&nbsp;&nbsp;Establish a website which depends on Django and PostgreSQL for real life business usage.
  
---
## Contents  
1. :books: Project Objective  
2. :closed_book:&nbsp;System Overview  
3. :green_book:&nbsp;System Diagram (UML diagram)  
4. :blue_book:&nbsp;Major Screen Capture  
5. :ledger:&nbsp;URLs Endpoint List  
---

## 1. :books: Project Objective
  
Establish an online bookstore where users can browse, search, add various books and related products to their shopping cart, and make purchases. The website will use Django as the backend web framework, providing functionalities for server-side logic, database interaction, user authentication, etc., to quickly create a secure and maintainable site. PostgreSQL will be used as the database, utilizing ORM to simplify queries and data access. By leveraging Django's MVT architecture, the process of database handling, user request processing, and model invocation to retrieve data will be accelerated, and the data will be passed to templates for rendering. This will streamline the front-end display and integrate the front-end and back-end work.
>建立一個書籍網購網站，使用戶可以瀏覽、搜索、添加到購物車和購買各種書籍及相關產品，並且能接受使用者增添產品評價及留言。網站將使用 Django 作為後端Web框架， 它提供處理伺服器端（後端）邏輯、資料庫互動、使用者認證等功能，快速建立安全、可維護的網站。同時以PostgreSQL 作為數據庫，使用ORM簡化查詢、存取資料庫等工作。利用Django的MVT架構加快資料庫處理、 處理使用者請求、調用Model 獲取資料，並將資料傳遞給Template 進行渲染 。簡化前端顯示部分的工作，一體化完成前後端工作。

-----

## 2. :closed_book: System Overview
  
#### ___Define project goals and feasibility scope.___
1. Configure the necessary tools and content based on client (ERB) requirements.
2. Establish an initial model prototype, including the front-end web server and architecture, Django server, database, and related libraries.
3. Budget work content and timeline, including team member responsibilities, processing content, and confirmation of each milestone.
4. Conduct mid- to late-stage system testing, deployment, and documentation.

>#### 釐定專案目標及可行性範圍:    
> 1. 根據客戶（ERB）要求配置各必須包含的工具及內容；  
> 2. 建立初始模型Prototype，包括前端網伺服器及架構，Django伺服器、資料庫及相關程式庫Library；  
> 3. 預算工作內容及時間，包括組員工作範圍、處理內容、各里程Milestone的確認；  
> 4. 中、後期系統測試，上線及文件記錄。
  

#### ___Design Contents:___
+ System design diagrams (UML).  
+ Front-end webpage design and relationship diagrams.  
+ Main design and functionality of the Django server.  
+ Database table design for PostgreSQL and related functional architecture.
+ Security testing and system maintenance plans.  

>#### 設計內容:  
> + 系統設計圖UML；  
> + 前端網頁設計及關聯示意圖；  
> + Django伺服器主程設計及功能；  
> + 資料庫PostgreSQL的資料表設計及相關功能架構；  
> + 安全測試及系統維護的預案。


-----


## 3. :green_book:&nbsp;System Diagram (UML diagram)   

  
Bookstore Class Diagram [Class Diagram](https://drive.google.com/file/d/1M11glC2JiXKmR2n2MO-sy5BBjudcUb5x/view?usp=drive_link).  
![erbBookstoreClassDiagram](https://github.com/user-attachments/assets/9d1673be-83f1-411a-9aa3-d1a0f51c2a91)


Level 0 and Level 1 Data Flow Diagram [DFD Diagram](https://drive.google.com/file/d/1z4tMEGNK0rV_89CbKIfXWD45JFGJ-o_V/view?usp=drive_link).  
![erbBookstoreDFDiagram](https://github.com/user-attachments/assets/1c4ea3b5-79f6-492d-a2f8-bd7d208b56ea)

Database Diagram [DB Diagram](https://drive.google.com/file/d/1uPw54sOVtur-MB6pNlOlpuNtivY_Bzju/view?usp=drive_link).  
![erbBookstoreDatabaseDiagram](https://github.com/user-attachments/assets/23f529ed-6b2c-4ced-b531-e8e0f3a53848)

-----

## 4. :blue_book:&nbsp;Major Screen Capture   

-----

  
## 5. :ledger:&nbsp;URLs Endpoint List  

___bookstore/urls.py___
Index endpoint: URL: /  
Admin endpoint: URL: /admin/  
Login endpoint: URL: /accounts/login/  
Logout endpoint: URL: /accounts/logout/  
Authenticated endpoint: URL: /accounts  

> ___books/urls.py___
> + Index endpoint: URL: “”
> + Book list endpoint: URL: /books/
> + Book list (by ID) endpoint: URL: /books/<int:book_id>/
> + Authors endpoint: URL: /authors/
> + Authors (by ID) endpoint: URL: /authors/<int:author_id>/
> + Genres endpoint: URL: /genres/
> + Genres (by ID) endpoint: URL: /genres/<int:genre_id>/
> + Register (User) endpoint: URL: /register/
> + User Profile endpoint: URL: /profile/
> + User Profile (Edit) endpoint: URL: /profile/edit/
> + Cart endpoint: URL: /cart/
> + Cart (Add Item) endpoint: URL: /cart/add/<int:book_id>/
> + Cart (Update Item) endpoint: URL: /cart/update/<int:book_id>/
> + Cart (Checkout) endpoint: URL: /checkout/
> + Orders endpoint: URL: /orders/
> + Orders (Details) endpoint: URL: /orders/<int:order_id>/
> + Orders (Cancel) endpoint: URL: /orders/<int:order_id>/cancel/




-----
That is so funny! :joy:


-----
