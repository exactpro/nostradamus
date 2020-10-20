import React from "react";
import { MessageSendingType, InboundReport } from "app/common/store/virtual-assistant/types";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import cn from "classnames";

interface MessageViewerFileUploadProps{
    report: InboundReport,
}

export default function MessageViewerFileUpload(props: MessageViewerFileUploadProps){
    return(
        <div className={cn("message-viewer-file-upload",`message-viewer-file-upload_${MessageSendingType.inbound}`)}>
            <a className={"message-viewer-file-upload__title"}
               href={props.report.link} download>

                <button className={"message-viewer-file-upload__button"}>
                    <Icon size={IconSize.normal} type={IconType.file}/>
                </button>
            </a>
            
            <div className={"message-viewer-file-upload__wrapper"}>
                
                <a className={"message-viewer-file-upload__title"}
                href={props.report.link} download>
                    {props.report.filename}
                </a>
                
                <div className="message-viewer-file-upload__info">
                
                <div className={"message-viewer-file-upload__info-title"}>
                    <p>{props.report.size}</p>
                    <p>{props.report.format}</p>
                </div>

                {
                    (props.report.filters && props.report.filters.project) &&
                    <div className={"message-viewer-file-upload__info-filters"}>
                    <p>{props.report.filters.project.join(", ")}</p>
                    </div>
                }
            
                </div>
            </div>
        </div>
    )
}