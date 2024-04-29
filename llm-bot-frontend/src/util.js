import ToastificationContent from "@core/components/toastification/ToastificationContent.vue";

const util = {
  data() {
    return {
      familyRelations: [
        { value: "Father", text: "Father" },
        { value: "Mother", text: "Mother" },
        { value: "Husband", text: "Husband" },
        { value: "Wife", text: "Wife" },
        { value: "Son", text: "Son" },
        { value: "Daughter", text: "Daughter" },
        { value: "Brother", text: "Brother" },
        { value: "Sister", text: "Sister" },
      ],
      propertyTypes: [
        { value: "Plot", text: "Plot" },
        { value: "Land", text: "Land" },
        { value: "House", text: "House" },
        { value: "Other", text: "Other" },
      ],
      armyPrefixs: [
        { value: "PA", text: "PA" },
        { value: "PS", text: "PS" },
      ],
      armyRanks: [
        { id: 1, name: "General" },
        { id: 2, name: "Lt. General" },
        { id: 3, name: "Maj. General" },
        { id: 4, name: "Brigadier" },
        { id: 5, name: "Colonel" },
        { id: 6, name: "Lt. Colonel" },
        { id: 7, name: "Major" },
        { id: 8, name: "Captain" },
        { id: 9, name: "Lieutenant" },
        { id: 10, name: "Second Lieutenant" },
        { id: 11, name: "Soldier/JCO" },
      ],
      petitionStatus: {
        PROCESSING: 1,
        CLOSED: 2,
      },
      petitionType: {
        GENERAL_OFFICER: 1,
        SENIOR_OFFICER: 2,
        OFFICER: 3,
        SOLDIER: 4,
      },
      categoryColors: {
        2: 'table-primary',
        3: 'table-info',
        4: 'bg-success',
        5: 'bg-warning',
      },
      priorityColors: {
        //'Flash': 'blinking'
      },
      engineeringParentCategories: [
        { id: 1, name: "Shaheed" },
        { id: 2, name: "War Wounded" },
        { id: 3, name: "Serving (incl LPR)" },
        { id: 4, name: "Retired/ISD" },
        { id: 5, name: "MES" },
        { id: 6, name: "PMAD" },
        { id: 7, name: "Def Paid Civ" },
      ],
      engineeringParentCategoriesDict: {
        1: "Shaheed",
        2: "War Wounded",
        3: "Serving (incl LPR)",
        4: "Retired/ISD",
        5: "MES",
        6: "PMAD",
        7: "Def Paid Civ",
      },
      seatTypes: [
        { value: 1, text: "Shaheed" },
        { value: 2, text: "War Wounded" },
        { value: 3, text: "Serving (incl LPR)" },
        { value: 4, text: "Retired/ISD" },
        { value: 5, text: "MES" },
        { value: 6, text: "PMAD" },
        { value: 7, text: "Def Paid Civ" },
      ],
      engineeringSeatTypeOptions: [
        { id: 1, name: "Shaheed" },
        { id: 2, name: "War Wounded" },
        { id: 3, name: "Serving (incl LPR)" },
        { id: 4, name: "Retired/ISD" },
        { id: 5, name: "MES" },
        { id: 6, name: "PMAD" },
        { id: 7, name: "Def Paid Civ" },
        { id: 8, name: "COAS Quota" },
        { id: 9, name: "Female Serving" },
        { id: 10, name: "Female Retired" },
        { id: 11, name: "PN" },
        { id: 12, name: "PAF" },
      ],
      medicalSeatTypeOptions: [
        { id: 1, name: "Shaheed" },
        { id: 2, name: "War Wounded" },
        { id: 3, name: "Serving (incl LPR)" },
        { id: 4, name: "Retired/ISD" },
        { id: 5, name: "Def Paid" },
      ],
      medicalSeatCategoryOptions: [
        { id: 1, name: "Normal" },
        { id: 2, name: "Self Financed" },
      ],
      medicalParentCategories: [
        { id: 1, name: "Shaheed" },
        { id: 2, name: "War Wounded" },
        { id: 3, name: "Serving (incl LPR)" },
        { id: 4, name: "Retired/ISD" },
        { id: 5, name: "Def Paid" },
      ],
      medicalParentCategoriesDict: {
        1: "Shaheed",
        2: "War Wounded",
        3: "Serving (incl LPR)",
        4: "Retired/ISD",
        5: "Def Paid",
      },
    };
  },
  methods: {
    displayError(error) {
      if (typeof error === "string") {
        this.$toast(
          {
            component: ToastificationContent,
            props: {
              title: "Error",
              icon: "BellIcon",
              text: error,
              variant: "danger",
            },
          },
          {
            timeout: 2000,
            position: "top-center",
          }
        );
        return;
      }

      let msgs = [];
      if (!error.response || error.response.status === 500) {
        msgs.push("Error: Network Error");
      } else if (error.response.status === 500) {
        msgs.push("Error: Server Error");
      } else if (typeof error.response.data === "string") {
        msgs.push("Error: Server Error");
      } else if (error.response.data.msg) {
        msgs.push(error.response.data.msg);
      } else {
        for (const key in error.response.data) {
          const element = error.response.data[key];
          if (Array.isArray(element)) {
            if (typeof element[0] === "string") {
              msgs.push(element[0]);
            } else if (typeof element[0] === "object") {
              for (const key in element[0]) {
                msgs.push(`${key}: ${element[0][key][0]}`);
              }
            }
          } else {
            msgs.push(element);
          }
        }
      }
      for (let i = 0; i < msgs.length; i++) {
        const msg = msgs[i];
        this.$toast(
          {
            component: ToastificationContent,
            props: {
              title: "Error",
              icon: "BellIcon",
              text: msg,
              variant: "danger",
            },
          },
          {
            timeout: 2000,
            position: "top-center",
          }
        );
      }
    },
    displayStatus(status) {
      let msg = "";
      switch (status) {
        case 0:
          msg = "Pending";
          break;
        case 1:
          msg = "Approved";
          break;
        case 2:
          msg = "Completed";
          break;
        case 3:
          msg = "Canceled";
          break;
        default:
          msg = "Pending";
          break;
      }
      return msg;
    },
    rowClass(item, type) {
      if (!item || type !== 'row') return
      return this.priorityColors[item.priority] + ' ' + this.categoryColors[item.category]
    },
    typeClass(type) {
      let color = "";
      switch (type) {
        case 1:
          color = "text-primary";
          break;
        case 2:
          color = "text-success";
          break;
        case 3:
          color = "text-info";
          break;
        case 4:
          color = "text-warning";
          break;
        default:
          break;
      }
      return color;
    },
    typeName(type) {
      let name = "";
      switch (type) {
        case 1:
          name = "Gen Offrs";
          break;
        case 2:
          name = "Brigs/Cols";
          break;
        case 3:
          name = "Lt Cols & below";
          break;
        case 4:
          name = "JCOs/Sldrs";
          break;
        default:
          break;
      }
      return name;
    },
    categoryClass(category) {
      let color = "";
      switch (category) {
        case 1:
          color = "table-primary";
          break;
        case 2:
          color = "table-success";
          break;
        case 3:
          color = "text-info";
          break;
        case 4:
          color = "table-warning";
          break;
        case 5:
          color = "table-dark";
          break;
      }
      return color;
    },
    categoryName(category) {
      let name = "";
      switch (category) {
        case 1:
          name = "Mk by COAS";
          break;
        case 2:
          name = "Mk By AG";
          break;
        case 3:
          name = "Normal";
          break;
        case 4:
          name = "Mk By Gen Offr";
          break;
        case 5:
          name = "Civs";
          break;
      }
      return name;
    },
  },
};

export default util;
