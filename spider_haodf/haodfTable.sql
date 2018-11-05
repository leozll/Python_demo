
CREATE TABLE [dbo].[Links](
	[Datetime] [datetime] default getdate(),
	[Type] [nvarchar](max) NULL,
	[Url] [nvarchar](max) NULL
) ON [PRIMARY]


CREATE TABLE [dbo].[facultyLog](
	[RunId] [int],
	[Url] [nvarchar](max) NULL,
	[Datetime] [datetime] default getdate()
) ON [PRIMARY]



CREATE TABLE [dbo].[Doctor](
	[id] [nvarchar](max) NULL,
	[Addr] [nvarchar](max) NULL,
	[Hospital] [nvarchar](max) NULL,
	[Department] [nvarchar](max) NULL,
	[Docname] [nvarchar](max) NULL,
	[ProfessionalTitle] [nvarchar](max) NULL,
	[AcademicTitle] [nvarchar](max) NULL,
	[BeGoodAt] [nvarchar](max) NULL,
	[PracticeExperience] [nvarchar](max) NULL,
	[ThanksLetter] [nvarchar](max) NULL,
	[Present] [nvarchar](max) NULL,
	[HeadIconUrl] [nvarchar](max) NULL,
	[ClinicalExperience] [nvarchar](max) NULL,
	[PatientsTreatedNumbers] [nvarchar](max) NULL,
	[PatientsFollowUpNumbers] [nvarchar](max) NULL,
	[DiagnosisServiceStar] [nvarchar](max) NULL,
	[PatientsVote] [nvarchar](max) NULL,
	[CurativeEffect] [nvarchar](max) NULL,
	[Attitude] [nvarchar](max) NULL,
	[PatientsQuestions] [nvarchar](max) NULL,
	[Replied] [nvarchar](max) NULL,
	[ServiceCharge] [nvarchar](max) NULL,
	[Mins] [nvarchar](max) NULL,
	[VisitsSuccess] [nvarchar](max) NULL,
	[Url] [nvarchar](max) NULL,
	[Datetime] [datetime] default getdate()
) ON [PRIMARY]




CREATE TABLE [dbo].[ExceptionLog](
	[RunId] [int],
	[Datetime] [datetime] default getdate(),
	[Exception] [nvarchar](max) NULL,
	[Message] [nvarchar](max) NULL,
	[Url] [nvarchar](max) NULL

) ON [PRIMARY]
