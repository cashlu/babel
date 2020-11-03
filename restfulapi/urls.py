from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from .views import CustomUserView, OrganizationView, DeviceStatusView, \
    ApplyRecordView, DevicesView, AppraisalTypeView, AppraisalPurposeView, FilePhaseView, \
    AppraisalFileView, AppraisalFileRecordView, AppraisalSampleView, LocaleFileView, \
    AdditionalFileView, MenusView, BasicInfoView, ApprInfoView, AppraisalFileImageView, \
    LocaleFileImageView, DeliveryStateView, AddiFileImageView, CheckRecordView, TodoListView, \
    DeviceGroupView, ApplyRecordDetailView, file_maker_view, FileMakerView

urlpatterns = [
    path('login/', obtain_jwt_token, name="用户认证"),
    # path("menus/", MenusView.as_view(), name="菜单列表"),
    # 获取或添加鉴定信息
    # path("apprinfos/", ApprInfoView.as_view(), name="鉴定信息列表"),
    # # 获取或更新一个鉴定信息
    # path("apprinfos/<int:pk>/", ApprInfoView.as_view(), name="鉴定信息"),
    path("filemaker/<int:basicInfoId>/", FileMakerView.as_view(), name="生成文件")
]

router = routers.SimpleRouter()
router.register(r"users", CustomUserView, basename="users")
router.register(r"orgs", OrganizationView, basename="orgs")
router.register(r"devstats", DeviceStatusView, basename="devstat")
router.register(r"applyrecs", ApplyRecordView, basename="applyrec")
router.register(r"applyrecdetail", ApplyRecordDetailView, basename="applyrecdetail")
router.register(r"devicegroup", DeviceGroupView, basename="devicegroup")
router.register(r"devices", DevicesView, basename="devices")
# router.register(r"applydevs", ApplyDeviceView, basename="applydev")
router.register(r"apprtypes", AppraisalTypeView, basename="apprtype")
router.register(r"apprpurps", AppraisalPurposeView, basename="apprpurp")
router.register(r"filephases", FilePhaseView, basename="filephase")
router.register(r"apprfiles", AppraisalFileView, basename="apprfile")
router.register(r"apprfileimgs", AppraisalFileImageView, basename="apprfileimgs")
router.register(r"apprfilerecs", AppraisalFileRecordView, basename="apprgilerecs")
router.register(r"apprsamps", AppraisalSampleView, basename="apprsamp")
router.register(r"localfiles", LocaleFileView, basename="localfiles")
router.register(r"localefileimages", LocaleFileImageView, basename="localefileimages")
router.register(r"addifiles", AdditionalFileView, basename="addifiles")
router.register(r"addifileimages", AddiFileImageView,basename="addifileimages")
router.register(r"basicinfos", BasicInfoView, basename="basicinfos")
router.register(r"deliverystates", DeliveryStateView, basename="deliverystates")
router.register(r"apprinfos", ApprInfoView, basename="apprinfos")
router.register(r"checkrecords", CheckRecordView, basename="checkrecords")
router.register(r"todo", TodoListView, basename="todolist")
router.register(r"menus", MenusView, basename="menus")
urlpatterns += router.urls
