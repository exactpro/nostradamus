import store from "app/common/store/configureStore";
import { Unsubscribe } from "redux";

export function checkIssuesExist(): Promise<boolean> {
  return new Promise<boolean>((resolve) => {

    let unsubscribeStore: Unsubscribe;

    if (store.getState().common.isLoadedIssuesStatus) {
      resolve(store.getState().common.isIssuesExist)
    } else {
      unsubscribeStore = store.subscribe(() => {
        if (store.getState().common.isLoadedIssuesStatus) {
          resolve(store.getState().common.isIssuesExist)
          unsubscribeStore()
        }
      })
    }

  })
}

export function checkModelIsFound(): Promise<boolean> {
  return new Promise<boolean>((resolve) => {

    let unsubscribeStore: Unsubscribe;

    if (store.getState().common.isSearchingModelFinished) {
      resolve(store.getState().common.isModelFounded)
    } else {
      unsubscribeStore = store.subscribe(() => {
        if (store.getState().common.isSearchingModelFinished) {
          resolve(store.getState().common.isModelFounded)
          unsubscribeStore()
        }
      })
    }

  })
}
