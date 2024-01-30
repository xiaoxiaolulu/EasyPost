<template>
  <el-card class="m-dept-side">
    <div class="title">
      <div v-show="switchProjectItem === false">
        <span class="avatar avatar-image" style="margin-left: 8px; margin-right: 6px;">
          <img :src=currentAvatar alt="">
        </span>
        <span style="display: inline-block; margin-left: 12px; font-weight: 400; font-size: 14px;">
                    {{ currentProjectName }}
                </span>
        <span @click="switchProjectItem = true"
              style="margin-left: 12px; cursor: pointer; line-height: 40px; color: #25b864">
                <el-icon><Sort/></el-icon>
        </span>
      </div>
      <el-select filterable style="margin: 0 auto; width: 180px" v-show="switchProjectItem"
                 placeholder="选择项目" v-model="projectItem">
        <el-option
            v-for="item in projectOption"
            :key="item.value"
            :label="item.label"
            :value="`${item.label},${item.value},${item.avatar}`">
        </el-option>
      </el-select>
    </div>
    <el-input v-model="filterText" placeholder="输入关键字进行过滤" class="filter-search"/>

    <div class="filter-tree">
      <el-scrollbar class="scrollbar">
        <el-tree
            ref="treeRef"
            :data="tableData"
            default-expand-all
            :filter-node-method="filterNode"
            @node-click="handleNodeClick"
        >
          <template #default="{ node, data }">
            <span class="custom-tree-node">
              <span><el-icon><Folder/></el-icon>&nbsp;&nbsp;{{ node.label }}</span>
              <el-dropdown style="float: right; color: #b6c1d0">
                <i><el-icon><More/></el-icon></i>
                <template #dropdown>
                  <el-dropdown-menu size="mini">
                  <el-dropdown-item @click.native="addDictsort">
                    <template #default="scope">
                      <i style="color: blue"><el-icon><Plus/></el-icon></i>
                      <span>添加目录</span>
                    </template>
                  </el-dropdown-item>
                  <el-dropdown-item @click.native="remove(node, data)">
                    <template #default="scope">
                      <i style="color: red"><el-icon><Delete/></el-icon></i>
                      <span>删除目录</span>
                    </template>
                  </el-dropdown-item>
                  <el-dropdown-item @click.native="editDictsort(data)">
                    <template #default="scope">
                      <i style="color: green"><el-icon><Edit/></el-icon></i>
                      <span>编辑目录</span>
                    </template>
                  </el-dropdown-item>
                </el-dropdown-menu>
                </template>
              </el-dropdown>
            </span>
          </template>
        </el-tree>
      </el-scrollbar>

    </div>
    <groupDialog ref="dialog"/>
  </el-card>
</template>

<script lang="ts" setup>
import {ref, watch} from 'vue'
import {ElMessage, ElMessageBox, ElTree} from "element-plus";
import groupDialog from './groupDialog.vue'
import {Plus, Sort, Folder, More, Delete, Edit} from "@element-plus/icons-vue";
import {getTree} from "@/api/http";

const emit = defineEmits(['change', 'switch'])

const tableData = ref<Tree[]>()
const dialog = ref(null)

interface Tree {
  id: string
  label: string
  children?: Tree[]
  parent: string
}


const filterText = ref('')

const treeRef = ref<InstanceType<typeof ElTree>>()

const projectOption = ref([])

const projectItem = ref("")

const currentProject = ref()

const currentAvatar = ref()

const currentProjectName = ref()

const switchProjectItem = ref(false)

const currentNode = ref()

const currentData = ref()

const pk = ref()

const maxId = ref()

const queryParams = ref({})

const setProjectList = (data) => {
  for (let i = 0; i < data.length; i++) {
    projectOption.value.push({
      "label": data[i]["name"],
      "value": data[i]["id"],
      "avatar": data[i]["avatar"]
    })
  }
  currentProjectName.value = data[0]["name"]
  currentProject.value = data[0]["id"]
  currentAvatar.value = data[0]["avatar"]
  switchProjectItem.value = false
  queryParams.value['currentProject'] = data[0]["id"]
}

const queryList = () => {
  getTree({
    id: currentProject.value,
    use_type: 1
  }).then((response) => {
    const {data, code, msg} = response.data
    tableData.value = data.tree
    pk.value = data.id
    maxId.value = data.maxId
  }).catch((error) => {
    ElMessage.error("获取接口目录数据失败;请重试！")
  })
}

// 监听输入
watch(filterText, (val) => {
  treeRef.value!.filter(val)
})

watch(projectItem, (value) => {
  switchProjectItem.value = false;
  let currentProjectList = value.split(",")
  currentProjectName.value = currentProjectList[0]
  currentProject.value = currentProjectList[1]
  currentAvatar.value = currentProjectList[2]
  queryList()
  emit('switch', currentProject)
  console.log('switch current ===========', currentProject.value)
})

// 搜索
const filterNode = (value: string, data: Tree) => {
  if (!value) return true
  return data.label.includes(value)
}

const addDictsort = () => {
  let item = {}
  item["pk"] = pk.value
  item["currentNode"] = currentNode.value
  item["treeData"] = tableData.value
  item["maxId"] = maxId.value
  dialog.value.show(item)
}

const editDictsort = (data: any) => {
  let item = {}
  item["pk"] = pk.value
  item["currentNode"] = currentNode.value
  item["currentData"] = currentData.value
  item["treeData"] = tableData.value
  item["maxId"] = maxId.value
  item["id"] = data.id
  dialog.value.show(item)
}

const selectAction = (node, data) => {
  // emit('change', data)
  console.log('node, data============', node, data)
}

const handleNodeClick = (node: any, data: any) => {
  currentNode.value = node
  currentData.value = data
  queryParams.value['node'] = node.id
  queryParams.value['date'] = data
  emit('change', queryParams)
  console.log('node, data============', node, data)
}

const remove = (node: any, data: any) => {
  ElMessageBox.confirm('你确定要删除当前项吗?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    draggable: true,
  }).then(() => {
    if (currentNode.value === '') {
      ElMessage.info('请选择一个节点')
      return
    } else {
      if (currentNode.value.label == '全部'){
        ElMessage.warning('根节点不可删除！')
        return
      }
      if (currentNode.value.children.length !== 0 ) {
        ElMessage.warning('此节点有子节点，不可删除！')
        return
      }
      else {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
        dialog.value.updateTrees(pk.value, tableData.value)
        ElMessage.success("删除分组成功");
      }
    }
  }).catch(() => {
    ElMessage.error("取消删除分组");
  })
  console.log('data===', node, data)
}

defineExpose({
  queryList,
  setProjectList
})
</script>

<style lang="scss" scoped>
@import "../index.scss";

.avatar {
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50%;
  margin-left: 8px;
  margin-right: 6px;
  box-sizing: border-box;
  padding: 0;
  color: rgba(0, 0, 0, .85);
  font-size: 13px;
  font-variant: tabular-nums;
  list-style: none;
  font-feature-settings: "tnum", "tnum";
  position: relative;
  display: inline-block;
  overflow: hidden;
  color: #fff;
  white-space: nowrap;
  text-align: center;
  vertical-align: middle;
  background: #ccc;
}

img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-image {
  background: transparent;
}

:deep(:focus-visible) {
  outline: none;
}
</style>
