import React from "react"; 
import "./popup-component.scss";

export enum ChildPosition{
    top = "top",
    bottom_right = "bottom_right",
}

interface PopupComponentProps{ 
    isChildDisplayed: boolean,
    childPosition: ChildPosition,
    parent: JSX.Element,
    child: JSX.Element
}

export default class PopupComponent extends React.Component<PopupComponentProps>{ 

    static defaultProps = {
        inScrollContainer: true,
        childPosition: ChildPosition.top,
    }

    parentRef: React.RefObject<HTMLDivElement> = React.createRef();
    childRef: React.RefObject<HTMLDivElement> = React.createRef();
    childCoords: any = {}; 
    timerID: number | undefined = undefined;

    componentDidMount = () => {
        this.childCoords = this.childRef.current!.getBoundingClientRect();
        this.calculateChildPosition();
    }   

    clearTimeout = () => {
        if(this.timerID){
            clearInterval(this.timerID);
            this.timerID = undefined;
        }    
    }

    componentDidUpdate = () => {
        
        clearTimeout();

        if(this.props.isChildDisplayed) this.timerID = setInterval(this.calculateChildPosition, 100);
        else clearTimeout();
    }

    calculateChildPosition = (isReturned: boolean = false) => { 
        let parentCoords: DOMRect | undefined  = this.parentRef.current?.getBoundingClientRect();
        let childCoeffs = this.getChildPositionCoeffs(parentCoords); 
       
        if(!parentCoords) return {};

        if(isReturned) return { top: parentCoords.top + childCoeffs.top, left: parentCoords.left + childCoeffs.left };
        this.childRef.current!.style.top = `${parentCoords.top + childCoeffs.top}px`;
        this.childRef.current!.style.left = `${parentCoords.left + childCoeffs.left}px`;  
    }

    getChildPositionCoeffs = (parentCoords: DOMRect | undefined) => {
        let childCoeffs = {top: 0, left: 0}  
        if(parentCoords) {
            switch (this.props.childPosition) {
                case ChildPosition.top:
                    return childCoeffs;
                case ChildPosition.bottom_right:
                    return {
                        top: parentCoords.height,
                        left: parentCoords.width - this.childCoords.width
                    }            
                default:
                    return childCoeffs;
            }
        }
        else return childCoeffs;
    }

    render(){    

        this.clearTimeout();
        
        return (
            <div className="pop-up-component">
                
                <div className="pop-up-component__parent" ref={this.parentRef}>
                    {this.props.parent}
                </div>
                
                <div className="pop-up-component__child" ref={this.childRef} style={this.calculateChildPosition(true)}>
                    {this.props.child}
                </div>
                    
            </div>
        )
    }
}  