import React, {Component} from "react";
import SlidingWindow from "app/common/components/sliding-window/sliding-window";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {activateVirtualAssistant} from "app/common/store/virtual-assistant/actions";
import {sendVirtualAssistantMessage} from "app/common/store/virtual-assistant/thunks";
import "app/modules/virtual-assistant/virtual-assistant.scss";
import MessageInput from "app/modules/virtual-assistant/message-input/message-input";
import MessageViewer from "app/modules/virtual-assistant/message-viewer/message-viewer"; 

class VirtualAssistant extends Component<Props>{

  state={
    message:"",
  }

  closeVirtualAssistant = () => {
    this.props.activateVirtualAssistant()
  }

  onInputMessage = (message: string) => {
    this.setState({message})
  }

  onSelectItem = (message: string) => () => {
    this.setState({message})
  }

  onSendMessage = () => {
    this.props.sendVirtualAssistantMessage(this.state.message)
    this.setState({message:""})
  }

  render(){
    return(
        <SlidingWindow title="Ask Nostradamus"
                       isOpen={this.props.isOpen}
                       onClose={this.closeVirtualAssistant}>

          <div className="virtual-assistant">
            <MessageViewer messages={this.props.messages}
                           selectItem={this.onSelectItem}/>
            <MessageInput message={this.state.message}
                          inputMessage={this.onInputMessage}
                          sendMessage={this.onSendMessage}/>
          </div>
        </SlidingWindow>
    )
  }
}

const mapStateToProps = ({virtualAssistant}: RootStore) => ({
    isOpen: virtualAssistant.isOpen,
    messages: virtualAssistant.messages,
})

const mapDispatchToProps = {
  activateVirtualAssistant,
  sendVirtualAssistantMessage,
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & {};

export default connector(VirtualAssistant);
