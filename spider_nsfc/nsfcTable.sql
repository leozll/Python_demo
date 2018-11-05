

CREATE TABLE [dbo].[nsfcLinkLog](
	[PidUrl] [nvarchar](max) NULL,
	[Page] [nvarchar](max) NULL,
	[Datetime] [datetime] default getdate()
) ON [PRIMARY]

CREATE TABLE [dbo].[nsfcEmptyLinkLog](
	[Datetime] [datetime] default getdate(),
	[Page] [nvarchar](max) NULL
) ON [PRIMARY]

CREATE TABLE [dbo].[PidInfo](
	[id] [nvarchar](max) NULL,
	[Datetime] [datetime] default getdate()
) ON [PRIMARY]


CREATE TABLE [dbo].[nsfcLinkInfo](
	[ProjectId] [int],
	[ProjectUrl] [nvarchar](max) NULL,
	[PeriodicalUrl] [nvarchar](max) NULL,
	[PeriodicalCount] [int],
	[ConferenceUrl] [nvarchar](max) NULL,
	[ConferenceCount] [int],
	[BookUrl] [nvarchar](max) NULL,
	[BookCount] [int],
	[RewardUrl] [nvarchar](max) NULL,
	[RewardCount] [int],
	[Page] [nvarchar](max) NULL,
	[Datetime] [datetime] default getdate()
) ON [PRIMARY]


CREATE TABLE [dbo].[ProjectInfo](
	[ProjectId] [int],
	[PID] [int],
	[ProjectName] [nvarchar](max) NULL,
	[ProjectType] [nvarchar](max) NULL,
	[ProjectCode] [nvarchar](max) NULL,
	[ProjectLeader] [nvarchar](max) NULL,
	[ProjectTitle] [nvarchar](max) NULL,
	[Organization] [nvarchar](max) NULL,
	[ProjectDuration] [nvarchar](max) NULL,
	[ProjectFunds] [nvarchar](max) NULL,
	[ChAbs] [nvarchar](max) NULL,
	[ChTitle] [nvarchar](max) NULL,
	[EngAbs] [nvarchar](max) NULL,
	[EngTitle] [nvarchar](max) NULL,
	[AbsTitle] [nvarchar](max) NULL,
	[Url] [nvarchar](max) NULL,
	[Datetime] [datetime] default getdate()
) ON [PRIMARY]

CREATE TABLE [dbo].[ExceptionLog](
	[RunId] [int],
	[Datetime] [datetime] default getdate(),
	[Exception] [nvarchar](max) NULL,
	[Message] [nvarchar](max) NULL,
	[Page] [nvarchar](max) NULL,
	[Url] [nvarchar](max) NULL
) ON [PRIMARY]
