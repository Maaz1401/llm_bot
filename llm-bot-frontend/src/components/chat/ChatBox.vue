  <template>
    <div
      class="h-100 d-flex align-items-center justify-content-center"
    >
        <!-- <b-col cols="1" class="h-100">
        </b-col> -->
        <b-col cols="1" sm="1" md="2" lg="2" xl="2" class="h-100">
            <!-- Content goes here -->
        </b-col>
        <b-col cols='10' xs='10' sm="10" md="8" lg="8" xl="8" class="h-100">
            <b-overlay :show="showOverlay" rounded="sm">
                <b-card class="h-100 w-100 p-1">
                    <vue-perfect-scrollbar
                        :settings="perfectScrollbarSettings"
                        class="scroll-area-size border border-primary"
                    >
                        <template>
                            <div 
                                v-for="(item, index) in messages"
                                :key="index"
                            >
                                <b-row v-if="item.message_type == 1">
                                    <div class="w-100">
                                        <div
                                        class="mb-1 rounded p-1 px-2"
                                        :class="{ 'float-right ml-5 bg-primary': item.role === 'user', 'float-left mr-5 bg-secondary': item.role === 'assistant' }"
                                        >
                                            {{item.content}}
                                        </div>
                                        <!-- <br/> -->
                                    </div>
                                </b-row>
                                <b-row v-if="item.message_type == 2">
                                    <div class="w-100">
                                        <div
                                        class="mb-1 rounded p-1 px-5"
                                        :class="{ 'float-right ml-5 bg-primary': item.role === 'user', 'float-left mr-5 bg-secondary': item.role === 'assistant' }"
                                        >
                                            <feather-icon
                                                icon="FileIcon"
                                                size="15"
                                            />
                                        </div>
                                        <!-- <br/> -->
                                    </div>
                                </b-row>
                            </div>
                            <div v-if="awaitingResponse">
                                <b-row>
                                    <div class="w-100">
                                        <div class="mb-1 rounded p-1 px-2 float-left mr-5 bg-secondary">
                                            <b-spinner small label="Small Spinner" type="grow" class="mr-1 ml-1"></b-spinner>
                                            <b-spinner small label="Small Spinner" type="grow" class="mr-1"></b-spinner>
                                            <b-spinner small label="Small Spinner" type="grow" class="mr-1"></b-spinner>
                                        </div>
                                        <!-- <br/> -->
                                    </div>
                                </b-row>
                            </div>
                        </template>
                    </vue-perfect-scrollbar>
                    <validation-observer ref="chatInputValidation">
                        <b-form @submit.prevent>
                            <b-row class="mt-2">
                                <b-col>
                                  <v-select id="messageType" inputId="id" label="text" v-model="selectedMessageType"
                                  :options="messageTypes" :clearable="false" placeholder="Message Type" class="border border-primary rounded" :disabled="awaitingResponse"/>
                                </b-col>                                
                            </b-row>
                            <b-row class="mt-2" v-if="selectedMessageType.id == 1">
                                <!-- <b-col >
                                    <validation-provider
                                        #default="{ errors }"
                                        name="chatMessage"
                                        rules="required"
                                    >
                                        <b-form-input
                                            id="message"
                                            v-model="message"
                                            :state="errors.length > 0 ? false : null"
                                            placeholder="Enter your message here"
                                        />
                                        <small class="text-danger">{{ errors[0] }}</small>
                                    </validation-provider>
                                    <b-button variant="primary">
                                        <feather-icon
                                            icon="ArrowUpIcon"
                                            size="15"
                                        />                             
                                    </b-button>                                
                                </b-col> -->
                                <!-- <b-col cols="2">
                                    <b-button variant="primary">
                                        <feather-icon
                                            icon="FilePlusIcon"
                                            size="15"
                                        />                             
                                    </b-button>
                                </b-col> -->
                                <b-col cols="10">
                                    <validation-provider
                                        #default="{ errors }"
                                        name="chatMessage"
                                    >
                                        <b-form-input
                                            id="message"
                                            v-model="message"
                                            :state="errors.length > 0 ? false : null"
                                            placeholder="Enter your message here"
                                            :disabled="awaitingResponse"
                                        />
                                        <small class="text-danger">{{ errors[0] }}</small>
                                    </validation-provider>
                                </b-col>
                                <b-col cols="2">
                                    <b-button variant="primary" block @click="updateUi" :disabled="awaitingResponse || message.length == 0">
                                        <feather-icon
                                            icon="ArrowUpIcon"
                                            size="15"
                                        />                             
                                    </b-button>
                                </b-col>
                            </b-row>
                            <b-row class="mt-1 mb-1" v-if="selectedMessageType.id == 2">
                                <b-col cols="10">
                                    <b-form-file v-model="file" class="mt-0" :state="Boolean(file)"
                                    accept=".pdf" @change="uploadFile($event)"
                                    placeholder="Upload file" drop-placeholder="Drop file here" ref="file"
                                    :disabled="awaitingResponse" 
                                    />
                                </b-col>
                                <b-col cols="2">
                                    <b-button variant="primary" block @click="updateUi" :disabled="awaitingResponse || !file">
                                        <feather-icon
                                            icon="ArrowUpIcon"
                                            size="15"
                                        />                             
                                    </b-button>
                                </b-col>
                                <!-- <template v-if="file">
                                    <b-col>
                                    <b-button size="md" class="mr-1 mt-2" @click="viewFile">
                                        <feather-icon icon="ExternalLinkIcon" size="16" class="mr-50" />
                                    </b-button>
                                    </b-col>
                                </template> -->
                            </b-row>                    
                        </b-form>
                    </validation-observer>    
                </b-card>
                <template #overlay>
                    <div v-if="chatsLoading">
                        <b-spinner variant="primary" label="Spinning"></b-spinner>
                    </div>
                    <div class="text-center" v-else>
                        <p id="cancel-label">Continue last converation?</p>
                        <b-button
                            ref="cancel"
                            variant="primary"
                            size="sm"
                            @click="continueLastConversation"
                            class="mr-2"
                        >
                            Yes
                        </b-button>
                        <b-button
                            ref="cancel"
                            variant="info"
                            size="sm"
                            aria-describedby="cancel-label"
                            @click="showOverlay = false"
                        >
                            Start a new conversation
                        </b-button>
                    </div>
                </template>
            </b-overlay>
        </b-col>
        <!-- <b-col cols="1" class="h-100">
        </b-col> -->
        <b-col cols='1' sm="1" md="2" lg="2" xl="2" class="h-100">
            <!-- Content goes here -->
        </b-col>
    </div>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import { $themeColors } from "@themeConfig";
  import moment from "moment";
  import util from "@/util.js";
  import "swiper/css/swiper.css";
  import VuePerfectScrollbar from "vue-perfect-scrollbar";
  import { ValidationProvider, ValidationObserver } from "vee-validate";
  import { required } from "@validations";
  
  export default {
    components: {
        VuePerfectScrollbar,
        ValidationProvider,
        ValidationObserver,
    },
    mixins: [util],
    data() {
      return {
        data: {},
        message: '',
        file: null,
        fileURL: '',
        perfectScrollbarSettings: {
            maxScrollbarLength: 150,
            wheelPropagation: false,
            useBothWheelAxes: false,
            suppressScrollX: true,
        },
        messages: [],
        session: null,
        newSession: true,
        // loadingAssistantContent: '.',
        awaitingResponse: false,
        chatsLoading: false,
        // awaitingResponseTimer: null,
        showOverlay: true,
        messageTypes: [
            {
                id: 1,
                text: "Text"
            },
            {
                id: 2,
                text: "Document"
            }
        ],
        selectedMessageType: null
      };
    },
    created() { 
        this.selectedMessageType = this.messageTypes[0]
    },
    async mounted() {
        // this.selectedMessageType = this.messageTypes[0]
    },
    methods: {
      ...mapActions({
        getLastConversation: "appData/getLastConversation",
        queryModel: "appData/queryModel",
      }),
      async continueLastConversation() {
        try {
            this.chatsLoading = true
            const res = await this.getLastConversation();
            this.messages = res.data.messages
            this.session = res.data.session
            if(this.session){
                this.newSession = false
            }
            else{
                this.newSession = true
            }
            this.chatsLoading = false
            this.showOverlay = false
        } catch (error) {
            this.chatsLoading = false
            this.showOverlay = false
            this.newSession = true
          this.displayError(error);
        }
      },
      viewFile() {
        window.open(this.fileURL, "_blank");
      },
      async uploadFile(event) {
        try {
            this.file = null;
            if (!event.target.files[0]) {
            return;
            }
            if (
            !(
                event.target.files[0].name.includes(".pdf")
            )
            ) {
            this.$refs.file.reset();
            this.$swal({
                title: "Please upload a PDF document",
                icon: "error",
            });
            return;
            }
            this.file = event.target.files[0];
            this.fileURL = URL.createObjectURL(this.file)
            // this.message = "Please explain the contents of this file."
        } catch (error) {
            this.displayError(error);
        }
      },
    //   waitingForResponse(){
    //     if(this.loadingAssistantContent.length < 3)
    //     {
    //         this.messages[this.messages.length - 1]
    //         this.loadingAssistantContent += this.loadingAssistantContent + '.'
    //     }
    //     else{
    //         this.loadingAssistantContent = '.'
    //     }
    //   },
      async updateUi(){
        if(this.selectedMessageType.id == 1)
        {
            this.messages.push(
                {
                    role: 'user',
                    content: this.message,
                    message_type: 1,
                }
            )
        }
        else if(this.selectedMessageType.id == 2)
        {
            this.messages.push(
                {
                    role: 'user',
                    message_type: 2,
                    // document: this.file,
                }
            )
        }

        this.awaitingResponse = true
        await this.submit()
      },
      async submit(){
        try {
          let formData = new FormData();

          let dataToInsert = {}  
          if(this.message){
            dataToInsert = {
                message: this.message,
            };
          }
          else if(this.file){
            formData.append("file", this.file);
          }

          this.file = null;
        //   this.$refs.file.reset();
          this.message = ''

          if(this.session){
            dataToInsert['session'] = this.session
          }
          else{
            this.newSession = true
            dataToInsert['new_session'] = true
          }

          formData.append("data", JSON.stringify(dataToInsert));

          const res = await this.queryModel(formData);
          if (res.status === 200) {
            this.awaitingResponse = false
            this.messages = res.data.messages
            this.newSession = false
            this.session = res.data.session
            // await this.resetModal();
            this.$nextTick(() => {
            });
            this.$emit("modalClosed");
          }
        } catch (error) {
          this.displayError(error);
        }
      }
    },
    computed: {
      ...mapGetters({
        hasPermission: "appData/hasPermission",
        getLoggedInUser: "appData/getLoggedInUser",
      }),
    },
    watch: {
        // async awaitingResponse(newValue, oldValue) {
        //     if(newValue){
        //         awaitingResponseTimer = setTimeout(waitingForResponse, milliseconds);
        //     }
        //     else{
        //         if(awaitingResponseTimer){
        //             clearTimeout(awaitingResponseTimer);
        //         }
        //     }
        // },
        selectedMessageType(newValue, oldValue)
        {
            if(newValue){
                if(newValue == 1)
                {
                    this.file = null;
                    this.$refs.file.reset();
                }
                else if(newValue == 1)
                {
                    this.message = ''
                }
            }
        }
    }
  };
  </script>
  
  <style>
    .scroll-area-size {
    height: 60vh;
    }

    .scroll-area-size ul {
    height: 100%;
    }  
   </style>
  