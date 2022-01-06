import React, {Component} from 'react';
import Dropzone from 'react-dropzone';
import './Classifier.css'
import {Alert, Button, Col, Container, Image, Row, Spinner} from 'react-bootstrap'
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
console.log("ALO: 161221-1515")
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true

const ImageData = [image_1, image_2, image_3, image_4, image_5,
    image_6, image_7, image_8, image_9, image_10, image_11, image_12,
    image_13, image_14, image_15, image_16, image_17, image_18,
    image_19, image_20, image_21]

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

        this.setState({
            files: [],
            isLoading: true,
            dropzone: null,
            recentImage: null,
            sample: true
        })

        this.loadImage({
            name: `${prefix}.png`,
            image: ImageData[`${prefix}`],
            backend_address: await fetch(ImageData[`${prefix}`]).then(res => res.blob()),
        })
    }

    onDrop = async (files) => {
        const object_image = URL.createObjectURL(files[0])

        this.setState({
            files: [],
            isLoading: true,
            dropzone: true,
            recentImage: null,
            sample: null,
            showUploaded: true,

        })

        this.loadImage({
            name: files[0].name,
            image: object_image,
            backend_address: await fetch(object_image).then(res => res.blob())
        })
    }

    loadImage = (files) => {
        setTimeout(() => {
            this.setState({
                files,
                showUploaded: true,
                isLoading: false
            }, () => {
                console.log(this.state.files)
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
        formData.append('picture', this.state.files.backend_address, this.state.files.name)
        axios.post(`${process.env.REACT_APP_AXIOS_URL}/api/async_image_analyze/`, formData, {
            headers: {
                'accept': 'application/json',
                'content-type': 'multipart/form-data'
            },
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
            recentImage: obj,
        })


        this.deactivateSpinner()
    }


    render() {

        const files = this.state.files.name

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
                            data-prefix="0"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 1
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="1"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 2
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="2"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 3
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="3"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 4
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="4"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 5
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="5"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 6
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="6"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 7
                        </button>
                    </Col>
                </Row>

                <Row className='mt-1'>
                    <Col sm>
                        <button
                            data-prefix="7"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 8
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="8"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 9
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="9"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 10
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="10"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 11
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="11"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 12
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="12"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 13
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="13"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 14
                        </button>
                    </Col>
                </Row>

                <Row className='mt-1'>
                    <Col sm>
                        <button
                            data-prefix="14"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 15
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="15"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 16
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="16"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 17
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="17"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 18
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="18"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 19
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="19"
                            onClick={(e) => this.handleClick(e)}
                            className="btn btn-primary">
                            Sample 20
                        </button>
                    </Col>
                    <Col sm>
                        <button
                            data-prefix="20"
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
                            {this.state.dropzone != null && this.state.showUploaded === true &&

                            <Image
                                src={this.state.files?.image}
                                height='400' rounded/>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        <div className="img-fluid">
                            {this.state.sample != null && this.state.showUploaded === true &&
                            <Image
                                src={this.state.files?.image}
                                height='400' rounded/>
                            }
                        </div>
                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {this.state.recentImage && this.state.showAnalyzed &&
                        <Image className='justify-content-center'


                               src={process.env.REACT_APP_AXIOS_URL + this.state.recentImage.data.analyzed_picture}
                               height='400' rounded/>

                        }

                        {this.state.recentImage && this.state.showOriginal &&
                        <Image className='justify-content-center'
                               src={this.state.files?.image}
                               height='400' rounded/>

                        }

                        {this.state.recentImage && this.state.showSegmented &&
                        <Image className='justify-content-center'
                               src={process.env.REACT_APP_AXIOS_URL + this.state.recentImage.data.segmented_image}
                               height='400' rounded/>

                        }


                    </Col>
                </Row>

                <Row>
                    <Col sm>
                        {this.state.dropzone != null && this.state.isLoading === false &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage}>
                            Analyze Image
                        </Button>}

                        {this.state.sample != null && this.state.isLoading === false &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage}>
                            Analyze Sample Image
                        </Button>}

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
