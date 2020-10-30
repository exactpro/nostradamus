import React from "react";
import { MessageSendingType, InboundReport } from "app/common/store/virtual-assistant/types";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import cn from "classnames";

interface MessageViewerFileUploadProps {
	report: InboundReport;
}

export default function MessageViewerFileUpload(props: MessageViewerFileUploadProps) {
	const { report } = props;

	return (
		<div
			className={cn(
				"message-viewer-file-upload",
				`message-viewer-file-upload_${MessageSendingType.inbound}`
			)}
		>
			<a className="message-viewer-file-upload__title" href={report.link} download>
				<button type="button" className="message-viewer-file-upload__button">
					<Icon size={IconSize.normal} type={IconType.file} />
				</button>
			</a>

			<div className="message-viewer-file-upload__wrapper">
				<a className="message-viewer-file-upload__title" href={report.link} download>
					{report.filename}
				</a>

				<div className="message-viewer-file-upload__info">
					<div className="message-viewer-file-upload__info-title">
						<p>{report.size}</p>
						<p>{report.format}</p>
					</div>

					{report.filters && report.filters.project && (
						<div className="message-viewer-file-upload__info-filters">
							<p>{report.filters.project.join(", ")}</p>
						</div>
					)}
				</div>
			</div>
		</div>
	);
}
