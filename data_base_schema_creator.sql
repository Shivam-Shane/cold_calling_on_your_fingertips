USE [cold_calling_emails]
GO
/****** Object:  Table [dbo].[cold_calling_details]    Script Date: 23-10-2024 17:52:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[cold_calling_details](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[your_name] [nvarchar](100) NOT NULL,
	[phone_no] [varchar](15) NOT NULL,
	[github_link] [nvarchar](255) NOT NULL,
	[linkedin_link] [nvarchar](255) NOT NULL,
	[portfolio_link] [nvarchar](255) NULL,
	[resume_path] [nvarchar](255) NULL,
	[last_updated] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[phone_no] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[sent_data_details]    Script Date: 23-10-2024 17:52:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[sent_data_details](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[subject] [nvarchar](255) NULL,
	[recipients] [nvarchar](255) NULL,
	[recipient_name] [nvarchar](255) NULL,
	[company_name] [nvarchar](255) NULL,
	[company_work_related] [nvarchar](255) NULL,
	[body] [nvarchar](max) NULL,
	[resume_path] [nvarchar](255) NULL,
	[created_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[cold_calling_details] ADD  DEFAULT (getdate()) FOR [last_updated]
GO
ALTER TABLE [dbo].[sent_data_details] ADD  DEFAULT (getdate()) FOR [created_at]
GO
