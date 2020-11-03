from django.shortcuts import get_object_or_404


class FileData:
    """
    A02     --      鉴定类别        --      BasicInfo.type.name
    A03     --      鉴定编号        --      BasicInfo.sn
    A04     --      鉴定用途        --      BasicInfo.purpose.name
    A05     --      委托人          --     BasicInfo.principal
    A06     --      委托事项        --      BasicInfo.trust_detail
    A07     --      是否重新鉴定     --      BasicInfo.is_re_appraisal
    A08     --      鉴定对象        --      BasicInfo.target
    A09     --      受理时间        --      BasicInfo.created_date
    A10     --      完成时间        --      FilePhase.finished_date
    A11     --      鉴定团队        --      AppraisalInfo.appraisal_team        列表(姓名)
    A12     --      复核人          --      AppraisalInfo.final_reviewer.name
    A13     --      主要鉴定意见     --      AppraisalInfo.opinion
    A14     --      立卷人          --      AppraisalInfo.archivist.name
    A15     --      归档日期        --      FilePhase.file_date
    A16     --      鉴定地址        --      AppraisalInfo.appraisal_address
    A17     --      基本案情        --      AppraisalInfo.project_detail
    A18     --      鉴定资料        --      AppraisalFile.objects.filter(basic_info=basic_info)    对象列表
    A19     --      送达状态        --      FilePhase.delivery.name
    A21     --      联系人          --     AppraisalInfo.contact
    A22     --      联系电话        --      AppraisalInfo.phone

    这个类用来封装用于前端生成docx的相关数据
    """

    def __init__(self, typename, sn, purpose, principal, trust_detail, is_re_appraisal, target,
                 created_date, finished_date, appraisal_team, final_reviewer, opinion, archivist,
                 file_date, appraisal_address, project_detail, delivery, contact, phone):
        self.typename = typename
        self.sn = sn
        self.purpose = purpose
        self.principal = principal
        self.trust_detail = trust_detail
        self.is_re_appraisal = is_re_appraisal
        self.target = target
        self.created_date = created_date
        self.finished_date = finished_date
        self.appraisal_team = appraisal_team
        self.final_reviewer = final_reviewer
        self.opinion = opinion
        self.archivist = archivist
        self.file_date = file_date
        self.appraisal_address = appraisal_address
        self.project_detail = project_detail
        self.delivery = delivery
        self.contact = contact
        self.phone = phone
