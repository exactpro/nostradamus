/* eslint-disable @typescript-eslint/no-floating-promises */
import React, { Component } from "react";
import SlidingWindow from "app/common/components/sliding-window/sliding-window";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { activateVirtualAssistant } from "app/common/store/virtual-assistant/actions";
import { sendVirtualAssistantMessage } from "app/common/store/virtual-assistant/thunks";
import "app/modules/virtual-assistant/virtual-assistant.scss";
import MessageInput from "app/modules/virtual-assistant/message-input/message-input";
import MessageViewer from "app/modules/virtual-assistant/message-viewer/message-viewer";

interface VirtualAssistantState {
	message: string;
}

class VirtualAssistant extends Component<VirtualAssistantProps, VirtualAssistantState> {
	constructor(props: VirtualAssistantProps) {
		super(props);
		this.state = {
			message: "",
		};
	}

	closeVirtualAssistant = () => {
		const { activateVirtualAssistant } = this.props;
		activateVirtualAssistant();
	};

	sendMessage = () => {
		const { sendVirtualAssistantMessage } = this.props;
		const { message } = this.state;
		sendVirtualAssistantMessage(message);
		this.setState({ message: "" });
	};

	inputMessage = (message: string) => {
		this.setState({ message });
	};

	selectMessageData = (item: string, renderItem?: string) => () => {
		const { sendVirtualAssistantMessage } = this.props;
		if (item.length) sendVirtualAssistantMessage(item, renderItem);
	};

	render() {
		const { messages, isOpen } = this.props;
		const { message } = this.state;
		return (
			<SlidingWindow title="Ask Nostradamus" isOpen={isOpen} onClose={this.closeVirtualAssistant}>
				<div className="virtual-assistant">
					<MessageViewer messages={messages} selectMessageData={this.selectMessageData} />
					<MessageInput
						message={message}
						inputMessage={this.inputMessage}
						sendMessage={this.sendMessage}
					/>
				</div>
			</SlidingWindow>
		);
	}
}

const mapStateToProps = ({ virtualAssistant }: RootStore) => ({
	isOpen: virtualAssistant.isOpen,
	messages: virtualAssistant.messages,
});

const mapDispatchToProps = {
	activateVirtualAssistant,
	sendVirtualAssistantMessage,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;
type VirtualAssistantProps = PropsFromRedux & unknown;

export default connector(VirtualAssistant);
