import React, {Component} from 'react';
import Dropzone from 'react-dropzone';
import './Classifier.css'
import {Spinner, Button, Alert, Image, Container, Row, Col} from 'react-bootstrap'
import axios from 'axios'
import image_1 from "../../static_media/1.png"
import image_2 from "../../static_media/2.png"
import image_3 from "../../static_media/3.png"
import image_4 from "../../static_media/4.png"
import image_5 from "../../static_media/5.png"
import image_6 from "../../static_media/6.png"
import image_7 from "../../static_media/7.png"
import image_8 from "../../static_media/8.png"
import image_9 from "../../static_media/9.png"
import image_10 from "../../static_media/10.png"
import image_11 from "../../static_media/11.png"
import image_12 from "../../static_media/12.png"
import image_13 from "../../static_media/13.png"
import image_14 from "../../static_media/14.png"
import image_15 from "../../static_media/15.png"
import image_16 from "../../static_media/16.png"
import image_17 from "../../static_media/17.png"
import image_18 from "../../static_media/18.png"
import image_19 from "../../static_media/19.png"
import image_20 from "../../static_media/20.png"
import image_21 from "../../static_media/21.png"

console.log(process.env.REACT_APP_AXIOS_URL)
console.log("ALO: 151121-1006")


class Classifier extends Component {

    state = {
        files: [],
        isLoading: false,
        recentImage: null,
        dropzone: null,
        sample: null,
        showAnalyzed: true,
        showSegmented: false,
        showOriginal: false,
        showUploaded: true,

    }

    show_original = () => {

        this.setState({
            showOriginal: true,
            showAnalyzed: false,
            showSegmented: false
        });
    }

    show_analyzed = () => {

        this.setState({
            showOriginal: false,
            showAnalyzed: true,
            showSegmented: false
        });
    }

    show_segmented = () => {

        this.setState({
            showOriginal: false,
            showAnalyzed: false,
            showSegmented: true
        });
    }

    handleClick = async (e) => {

        const prefix = e.target.dataset.prefix;
        const ImageData = [image_1, image_2, image_3, image_4, image_5,
            image_6, image_7, image_8, image_9, image_10, image_11, image_12,
            image_13, image_14, image_15, image_16, image_17, image_18,
            image_19, image_20, image_21]

        const FILES = {
            "image_1": [{
                name: "1.png",
                image: ImageData[0],
                backend_address: await fetch(ImageData[0]).then(res => res.blob())
            }],
            "image_2": [{
                name: "2.png",
                image: ImageData[1],
                backend_address: await fetch(ImageData[1]).then(res => res.blob())

            }],
            "image_3": [{
                name: "3.png",
                image: ImageData[2],
                backend_address: await fetch(ImageData[2]).then(res => res.blob())

            }],
            "image_4": [{
                name: "4.png",
                image: ImageData[3],
                backend_address: await fetch(ImageData[3]).then(res => res.blob())

            }],
            "image_5": [{
                name: "5.png",
                image: ImageData[4],
                backend_address: await fetch(ImageData[4]).then(res => res.blob())

            }],
            "image_6": [{
                name: "6.png",
                image: ImageData[5],
                backend_address: await fetch(ImageData[5]).then(res => res.blob())

            }],
            "image_7": [{
                name: "7.png",
                image: ImageData[6],
                backend_address: await fetch(ImageData[6]).then(res => res.blob())

            }],
            "image_8": [{
                name: "8.png",
                image: ImageData[7],
                backend_address: await fetch(ImageData[7]).then(res => res.blob())

            }],
            "image_9": [{
                name: "9.png",
                image: ImageData[8],
                backend_address: await fetch(ImageData[8]).then(res => res.blob())

            }],
            "image_10": [{
                name: "10.png",
                image: ImageData[9],
                backend_address: await fetch(ImageData[9]).then(res => res.blob())

            }],
            "image_11": [{
                name: "11.png",
                image: ImageData[10],
                backend_address: await fetch(ImageData[10]).then(res => res.blob())

            }],
            "image_12": [{
                name: "12.png",
                image: ImageData[11],
                backend_address: await fetch(ImageData[11]).then(res => res.blob())

            }],
            "image_13": [{
                name: "13.png",
                image: ImageData[12],
                backend_address: await fetch(ImageData[12]).then(res => res.blob())

            }],
            "image_14": [{
                name: "14.png",
                image: ImageData[13],
                backend_address: await fetch(ImageData[13]).then(res => res.blob())

            }],

            "image_15": [{
                name: "15.png",
                image: ImageData[14],
                backend_address: await fetch(ImageData[14]).then(res => res.blob())

            }],
            "image_16": [{
                name: "16.png",
                image: ImageData[15],
                backend_address: await fetch(ImageData[15]).then(res => res.blob())

            }],
            "image_17": [{
                name: "17.png",
                image: ImageData[16],
                backend_address: await fetch(ImageData[16]).then(res => res.blob())

            }],
            "image_18": [{
                name: "18.png",
                image: ImageData[17],
                backend_address: await fetch(ImageData[17]).then(res => res.blob())

            }],
            "image_19": [{
                name: "19.png",
                image: ImageData[18],
                backend_address: await fetch(ImageData[18]).then(res => res.blob())

            }],
            "image_20": [{
                name: "20.png",
                image: ImageData[19],
                backend_address: await fetch(ImageData[19]).then(res => res.blob())

            }],
            "image_21": [{
                name: "21.png",
                image: ImageData[20],
                backend_address: await fetch(ImageData[20]).then(res => res.blob())

            }],
        }

        this.setState({
            files: [],
            isLoading: true,
            recentImage: null,
            dropzone: null,
            sample: true
        })
        this.loadImage(FILES[`image_${prefix}`])
    }

    onDrop = async (files) => {
        const object_image = URL.createObjectURL(files[0])
        console.log(files[0].name)

        const FILES = {
            "uploaded_image": [{
                name: files[0].name,
                image: object_image,
                backend_address: await fetch(object_image).then(res => res.blob())
            }]
        }

        this.setState({
            files: [],
            isLoading: true,
            dropzone: true,
            sample: null,
            recentImage: null
        })
        this.loadImage(FILES["uploaded_image"])
    }

    loadImage = (files) => {
        setTimeout(() => {
            this.setState({
                files,
                isLoading: false
            }, () => {
                console.log(this.state.files[0])
            })
        }, 1000);
    }

    activateSpinner = () => {
        this.setState({
            isLoading: true,
        })
    }

    deactivateSpinner = () => {
        this.setState({
            isLoading: false,
        })
    }


    sendImage = () => {


        this.activateSpinner()
        let formData = new FormData()
        formData.append('picture', this.state.files[0].backend_address, this.state.files[0].name)
        axios.post(`${process.env.REACT_APP_AXIOS_URL}/api/analyze_im/`, formData, {
            headers: {
                'accept': 'application/json',
                'content-type': 'multipart/form-data'
            }
        })
            .then(resp => {
                console.log(resp)
                this.getStatus(resp)
            })
            .catch(err => {
                console.log(err.response)
            })
    }

    getStatus = (obj) => {
        axios.get(`${process.env.REACT_APP_AXIOS_URL}/api/task/${obj.data.task_id}/`,
            {
                headers: {
                    'accept':
                        'application/json',
                }
            },
        ).then(resp => {
            (resp.data.task_status === 'PENDING') ? this.getStatus(resp) : this.getImageClass(resp)
            console.log(resp.data.task_status)

        })
            .catch(err => {
                console.log(err.response)
            })

    }

    getImageClass = (obj) => {

        this.setState({
            showUploaded: false,
            isLoading: false,
        })


        axios.get(`${process.env.REACT_APP_AXIOS_URL}/api/analyze_im/${obj.data.id}/`,
            {
                headers: {
                    'accept':
                        'application/json',
                }
            },
        )
            .then(resp => {
                this.setState({recentImage: resp})
            })
            .catch(err => {
                console.log(err.response.data)
            })
        this.deactivateSpinner()
    }


    render() {

        const files = this.state.files.map(file => (
            <li key={file.name}>
                {file.name}
            </li>
        ));
        return (


            <Container>

                <Row>
                    <Col sm={12}>
                        <Dropzone onDrop={this.onDrop} accept='image/png, image/jpeg'>
                            {({isDragActive, getRootProps, getInputProps}) => (
                                <div {...getRootProps({className: 'dropzone back'})}>
                                    <input {...getInputProps()} />
                                    <i className="far fa-image mb-2 text-muted" style={{fontSize: 100}}></i>
                                    <p className='text-muted'>{isDragActive ? "Drop some images " : "Drag 'n' drop some files here, or click to select files"}</p>
                                </div>
                            )}
                        </Dropzone>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <button
                            data-prefix="1"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 1
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="2"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 2
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="3"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 3
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="4"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 4
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="5"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 5
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="6"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 6
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="7"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 7
                        </button>
                    </Col>
                </Row>

                <Row className='mt-1'>
                    <Col sm>
                        <button
                            data-prefix="8"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 8
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="9"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 9
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="10"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 10
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="11"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 11
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="12"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 12
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="13"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 13
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="14"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 14
                        </button>
                    </Col>
                </Row>

                <Row className='mt-1'>
                    <Col sm>
                        <button
                            data-prefix="15"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 15
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="16"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 16
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="17"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 17
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="18"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 18
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="19"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 19
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="20"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 20
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="21"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 21
                        </button>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <div className="mt-2">
                            {
                                this.state.isLoading &&
                                <Spinner animation="border" role="status"></Spinner>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <aside>
                            {files}
                        </aside>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {
                            this.state.recentImage &&
                            <button
                                onClick={this.show_original}
                                className="btn btn-success">
                                Original Image
                            </button>
                        }
                    </Col>
                    <Col sm>
                        {
                            this.state.recentImage &&
                            <button
                                onClick={this.show_analyzed}
                                className="btn btn-success">
                                Analyzed Image
                            </button>
                        }
                    </Col>
                    <Col sm>
                        {
                            this.state.recentImage &&
                            <button
                                onClick={this.show_segmented}
                                className="btn btn-success">
                                Segmented Image
                            </button>
                        }
                    </Col>

                </Row>

                <Row>
                    <Col sm>
                        <div className="img-fluid mt-2">
                            {this.state.files.length > 0 && this.state.dropzone != null && this.state.showUploaded === true &&

                            <Image
                                src={this.state.files[0].image}
                                height='400' rounded/>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <div className="img-fluid">
                            {this.state.files.length > 0 && this.state.sample != null && this.state.showUploaded === true &&
                            <Image
                                src={this.state.files[0].image}
                                height='400' rounded/>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {this.state.recentImage && this.state.showAnalyzed &&
                        <Image className='justify-content-center'
                               src={this.state.recentImage.data.analyzed_picture}
                               height='400' rounded/>

                        }

                        {this.state.recentImage && this.state.showOriginal &&
                        <Image className='justify-content-center'
                               src={this.state.files[0].image}
                               height='400' rounded/>

                        }

                        {this.state.recentImage && this.state.showSegmented &&
                        <Image className='justify-content-center'
                               src={this.state.recentImage.data.segmented_image}
                               height='400' rounded/>

                        }


                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {this.state.files.length > 0 && this.state.dropzone != null &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage}>Analyze
                            Image </Button>}

                        {this.state.files.length > 0 && this.state.sample != null &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage}>Analyze
                            Sample
                            Image </Button>}

                        {
                            this.state.recentImage &&
                            <div className="mt-2">
                                <Alert variant='primary'>
                                    <p> Time Taken: {this.state.recentImage.data.time_to_classify} </p>
                                    <p> Number of Capillaries: {this.state.recentImage.data.number_of_capillaries} </p>
                                    <p> Capillary Density : {this.state.recentImage.data.capillary_area} (1 pixel =
                                        2.2µm) </p>

                                </Alert>
                            </div>
                        }
                    </Col>
                </Row>

            </Container>


        )
    }
}

export default Classifier;


